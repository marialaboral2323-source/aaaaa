.intel_syntax noprefix
.section .text
.global _start
_start:
  lea rsp, [rip + 0x200]
  and rsp, -16

  lea rsi, [rip]      # points into this shellcode (always mapped)
  mov edx, 4
  mov eax, 1
  mov edi, 1
  syscall

  mov eax, 60
  xor edi, edi
  syscall
