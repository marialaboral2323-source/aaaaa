.syntax unified
.thumb
.global _start
_start:
  ldr r0, =0x4000c000      /* UART0DR */
  movs r1, #'O'
  strb r1, [r0]
  movs r1, #'K'
  strb r1, [r0]
1:
  b 1b

