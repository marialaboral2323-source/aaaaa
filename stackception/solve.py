#!/usr/bin/env python3
import socket
import struct
import time

def create_binary_with_opcode11():
    """Crear binario con opcode 11 directamente"""
    with open('/tmp/exploit_op11.bin', 'wb') as f:
        f.write(struct.pack('<I', 11))  # opcode 11
        f.write(struct.pack('<I', 0))    # argumento
    return '/tmp/exploit_op11.bin'

def test_local():
    """Probar localmente"""
    import subprocess
    bin_path = create_binary_with_opcode11()
    result = subprocess.run(['./stackception-1', bin_path], 
                          capture_output=True, text=True, timeout=10)
    print("Resultado local:", result.stderr)

if __name__ == '__main__':
    # El problema es que necesito pasar el opcode 11 a través de chall.py
    # Pero chall.py ejecuta stackception-asm primero, que no reconoce opcode 11
    # Necesito encontrar una forma de hacer que stackception-asm genere opcode 11
    # O modificar el binario después de compilarlo
    
    print("Analizando...")
    test_local()
