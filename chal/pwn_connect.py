#!/usr/bin/env python3
import re
import socket
import subprocess
import sys
import time
from typing import List, Tuple


HOST = "5.75.155.137"
PORT = 1338


POW_RE = re.compile(r'unhex\("([0-9a-fA-F]+)" \+ S\)\)\s+ends with\s+(\d+)\s+zero bits')


def recv_until(sock: socket.socket, delim: bytes, limit: int = 1_000_000) -> bytes:
    buf = bytearray()
    while delim not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            break
        buf += chunk
        if len(buf) > limit:
            break
    return bytes(buf)


def parse_pow(line: str) -> Tuple[str, int]:
    m = POW_RE.search(line)
    if not m:
        raise ValueError(f"can't parse pow line: {line!r}")
    prefix_hex = m.group(1)
    zero_bits = int(m.group(2))
    return prefix_hex, zero_bits


def solve_pow(prefix_hex: str, zero_bits: int) -> str:
    # Use the compiled C solver for speed.
    p = subprocess.run(
        ["/workspace/chal/pow_solver", prefix_hex, str(zero_bits)],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=300,
        check=True,
        text=True,
    )
    return p.stdout.strip()


def main() -> int:
    sock = socket.create_connection((HOST, PORT), timeout=10)
    sock.settimeout(10)

    banner = recv_until(sock, b"\n", limit=10000).decode(errors="replace")
    prefix_hex, zero_bits = parse_pow(banner)
    s_hex = solve_pow(prefix_hex, zero_bits)
    sock.sendall((s_hex + "\n").encode())

    # If extra lines are provided on argv, send them as oracle "questions".
    to_send: List[bytes] = []
    if len(sys.argv) > 1:
        for s in sys.argv[1:]:
            if s.startswith("hex:"):
                raw = bytes.fromhex(s[4:])
                to_send.append(raw + b"\n")
            else:
                to_send.append((s + "\n").encode())

    buf = bytearray()
    sock.settimeout(0.2)
    last = time.time()
    send_idx = 0
    while True:
        # opportunistically send next line after we see a prompt, or if no prompt
        # is recognized, just send sequentially with small delays.
        if send_idx < len(to_send):
            if b"Please ask your question" in buf or (time.time() - last) > 1.0:
                sock.sendall(to_send[send_idx])
                send_idx += 1
                last = time.time()

        try:
            out = sock.recv(65536)
        except socket.timeout:
            if (time.time() - last) > 5.0 and send_idx >= len(to_send):
                break
            continue
        if not out:
            break
        buf += out
        sys.stdout.buffer.write(out)
        sys.stdout.buffer.flush()
        last = time.time()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

