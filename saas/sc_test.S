.intel_syntax noprefix
.section .text
.global _start
_start:
  lea rsp, [rip + 0x200]
  and rsp, -16

  lea rsi, [rip + msg]
  mov edx, 3
  mov eax, 1
  mov edi, 1
  syscall

  mov eax, 60
  xor edi, edi
  syscall

msg:
  .ascii "HI\\n"
