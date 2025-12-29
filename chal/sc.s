# x86_64 shellcode (GAS Intel syntax) for emu.py
# WIP: will iterate until <42 bytes and passes.

.intel_syntax noprefix
.global _start
_start:
    # rdi=out, rsi=in, rdx=len (44)
    mov cl, 11              # 11 groups of 4 chars

gloop:
    xor ebx, ebx
    mov dl, 4

iloop:
    lodsb

    # map base64 char in AL -> 6-bit value in AL
    # (attempt, not optimized yet)
    sub al, 65
    cmp al, 26
    jb mapped
    sub al, 6
    cmp al, 52
    jb mapped
    add al, 75
    cmp al, 52
    jae mapped
    shr al, 2
    add al, 51

mapped:
    shl ebx, 6
    or bl, al
    dec dl
    jnz iloop

    # pack 24 bits in ebx -> write 3 bytes to [rdi]
    bswap ebx
    shr ebx, 8
    mov [rdi], ebx
    add edi, 3

    dec cl
    jnz gloop

    # done (fall off / stop)
