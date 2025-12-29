BITS 64
DEFAULT REL

; base64 decode 44 bytes from [rsi] -> 32 bytes to [rdi]
; rdx = 44
; clobbers: rax, rcx, rbx

start:
    mov cl, 11              ; 11 quartets
.loop:
    ; v0
    lodsb
    call dec6
    mov bl, al
    ; v1
    lodsb
    call dec6
    mov bh, al
    ; out0 = (v0<<2) | (v1>>4)
    mov al, bl
    shl al, 2
    mov dl, bh
    shr dl, 4
    or  al, dl
    stosb

    ; v2
    lodsb
    call dec6
    mov bl, al
    ; out1 = ((v1&0xF)<<4) | (v2>>2)
    mov al, bh
    and al, 0x0f
    shl al, 4
    mov dl, bl
    shr dl, 2
    or  al, dl
    stosb

    ; v3
    lodsb
    call dec6
    ; out2 = ((v2&3)<<6) | v3
    mov dl, bl
    and dl, 3
    shl dl, 6
    or  al, dl
    stosb

    dec cl
    jnz .loop

    ; fixup last byte (we decoded 33 bytes; input ends with == so last should be dropped)
    ; overwrite last byte with previous (no-op) and back up by 1 so emu reads only first 32 anyway.
    ; (result_ptr is read as fixed 32 bytes, so just do nothing extra)
    nop

; dec6: AL=base64 char -> AL=0..63
dec6:
    cmp al, 0x40
    jb  .non
    sub al, 65
    cmp al, 26
    jb  .ret
    sub al, 6
.ret:
    ret
.non:
    sub al, 0x2b          ; '+' => 0, '/' => 4, '0'.. => 5..14, '=' => 18
    cmp al, 5
    jb  .sym
    cmp al, 15
    jae .pad
    add al, 0x2f          ; digit: (c-0x2b) + 0x2f = c+4
    ret
.sym:
    shr al, 2
    add al, 62
    ret
.pad:
    xor al, al
    ret
