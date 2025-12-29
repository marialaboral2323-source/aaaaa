.syntax unified
.thumb
.global _start

_start:
    /* Load MMIO addresses without literal pool to avoid 0x0a bytes. */
    movw r4, #0xD018      /* UART1_FR */
    movt r4, #0x4000
    movw r5, #0xD000      /* UART1_DR */
    movt r5, #0x4000
    movw r6, #0xC018      /* UART0_FR */
    movt r6, #0x4000
    movw r7, #0xC000      /* UART0_DR */
    movt r7, #0x4000

    /* Marker: print 'OK!' on UART0 so we know we executed. */
    movs r0, #0x4f        /* 'O' */
1:  ldr  r1, [r6]
    tst  r1, #0x20
    bne  1b
    str  r0, [r7]
    movs r0, #0x4b        /* 'K' */
2:  ldr  r1, [r6]
    tst  r1, #0x20
    bne  2b
    str  r0, [r7]
    movs r0, #0x21        /* '!' */
3:  ldr  r1, [r6]
    tst  r1, #0x20
    bne  3b
    str  r0, [r7]

loop:
    ldr r0, [r4]
    tst r0, #0x10        /* RXFE */
    bne loop

    ldr r0, [r5]         /* byte in low bits */
    uxtb r0, r0

txwait:
    ldr r1, [r6]
    tst r1, #0x20        /* TXFF */
    bne txwait
    str r0, [r7]

    cmp r0, #0x7d        /* '}' */
    bne loop

hang:
    b hang

