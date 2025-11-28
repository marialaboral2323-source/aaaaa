#!/usr/bin/env python3
with open('/workspace/challenge/rev_sepc/extracted/checker.ko', 'rb') as f:
    data = f.read()

rodata_start = 0x3e0
array1_offset = rodata_start + 0x20  # 0x400
array2_offset = rodata_start + 0x60  # 0x440

# Leer los arrays
array1 = data[array1_offset:array1_offset+33]
array2 = data[array2_offset:array2_offset+33]

key = bytes([array2[i] ^ array1[i] for i in range(33)])
print(f"Key: {key.hex()}")
print(f"Key as ASCII: {key.decode('ascii', errors='ignore')}")

# El código verifica 33 bytes exactos
# La flag parece ser: HTB{grabbing_d4t4_fr0m_k3rn3l5p4c
# Pero normalmente las flags terminan con }
# Tal vez el } está implícito o la flag realmente termina en c

# Intentar con }
flag_with_brace = key.decode('ascii', errors='ignore') + '}'
print(f"\nFlag con cierre: {flag_with_brace}")
