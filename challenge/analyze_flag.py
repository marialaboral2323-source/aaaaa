#!/usr/bin/env python3
with open('/workspace/challenge/rev_sepc/extracted/checker.ko', 'rb') as f:
    data = f.read()

rodata_start = 0x3e0
array1_offset = rodata_start + 0x20
array2_offset = rodata_start + 0x60

# Probar con diferentes longitudes
for length in [32, 33, 34]:
    array1 = data[array1_offset:array1_offset+length]
    array2 = data[array2_offset:array2_offset+length]
    
    key = bytes([array2[i] ^ array1[i] for i in range(length)])
    print(f"Length {length}: {key.decode('ascii', errors='ignore')}")
    
    # Buscar el cierre de la flag
    if b'}' in key:
        end_idx = key.index(b'}')
        flag = key[:end_idx+1].decode('ascii')
        print(f"  -> Flag completa: {flag}")

# Buscar '}' en el archivo
if b'}' in data:
    idx = data.find(b'}')
    print(f"\nEncontrado '}' en offset: {hex(idx)}")
    print(f"Contexto: {data[idx-10:idx+10].hex()}")

# Probar si el último byte debería ser diferente
print("\nÚltimos bytes de los arrays:")
for i in range(30, 35):
    if array1_offset + i < len(data) and array2_offset + i < len(data):
        b1 = data[array1_offset + i]
        b2 = data[array2_offset + i]
        result = b2 ^ b1
        char = chr(result) if 32 <= result < 127 else '?'
        print(f"Byte {i}: array1={hex(b1)}, array2={hex(b2)}, result={hex(result)} = '{char}'")
