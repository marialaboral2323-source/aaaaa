#!/usr/bin/env python3

import base64
import secrets

import unicorn
import unicorn.unicorn_const
import unicorn.x86_const


def main(code):
    assert len(code) < 42, "Too long :("

    emu = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)

    code_ptr   = 0x10000000
    alloc_size = 0x10000000

    emu.mem_map(code_ptr, alloc_size)
    emu.mem_write(code_ptr, code)

    # input
    secret = secrets.token_bytes(32)
    b64_secret = base64.b64encode(secret)

    # IN and OUT arrays
    secret_ptr   = 0x20000000
    result_ptr = 0x20010000

    emu.mem_map(secret_ptr, alloc_size)
    emu.mem_write(secret_ptr, b64_secret)

    # calling convention similar to memcpy
    # base64decode(void* out, void* in, unsigned len)
    # out
    emu.reg_write(unicorn.x86_const.UC_X86_REG_RDI, result_ptr)
    # in
    emu.reg_write(unicorn.x86_const.UC_X86_REG_RSI, secret_ptr)
    # len
    emu.reg_write(unicorn.x86_const.UC_X86_REG_RDX, len(b64_secret))

    # stack
    stack_ptr = 0x30000000
    emu.mem_map(stack_ptr, alloc_size)
    emu.reg_write(unicorn.x86_const.UC_X86_REG_RSP, stack_ptr + alloc_size)

    try:
        emu.emu_start(
            begin=code_ptr,
            until=code_ptr + len(code),
            timeout=1 * unicorn.unicorn_const.UC_SECOND_SCALE,
            count=2000)
    except:
        # ignore all errors
        pass

    result = bytes(emu.mem_read(result_ptr, 32))
    if result == secret:
        print("Congratulations, here's your flag:")
        with open("flag.txt", "r") as f:
            print(f.read())
    else:
        print(":(")

if __name__ == "__main__":
    code = input("Please give your shellcode as hex:\n")
    main(bytes.fromhex(code))
