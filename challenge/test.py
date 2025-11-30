#!/usr/bin/env python3
import socket
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('dyn06.heroctf.fr', 13683))

def recv_until(s, text):
    data = b''
    while text not in data:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
            sys.stdout.write(chunk.decode('utf-8', errors='ignore'))
            sys.stdout.flush()
        except socket.timeout:
            break
    return data.decode('utf-8', errors='ignore')

try:
    # Recibir menú inicial
    recv_until(s, b'> ')
    
    # Opción 1: Submit story
    s.send(b'1\n')
    recv_until(s, b': ')
    
    # Enviar longitud
    s.send(b'64\n')
    recv_until(s, b': ')
    
    # Enviar historia
    story = "A" * 64
    s.send(story.encode() + b'\n')
    time.sleep(1)
    recv_until(s, b'> ')
    
    # Ver resultados
    s.send(b'4\n')
    time.sleep(1)
    result = recv_until(s, b'> ')
    
    # Ver última historia
    s.send(b'2\n')
    time.sleep(1)
    recv_until(s, b'> ')
    
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()
