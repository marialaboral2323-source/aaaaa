#!/usr/bin/env python3
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
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
            print(chunk.decode('utf-8', errors='ignore'), end='', flush=True)
        except socket.timeout:
            break
    return data.decode('utf-8', errors='ignore')

# Menú
recv_all(s)

# Submit story
s.send(b'1\n')
recv_all(s)

# Length
s.send(b'64\n')
recv_all(s)

# Story
story = "Once upon a time, there was a flag waiting to be found."
s.send(story.encode() + b'\n')
print("\n--- Story sent, waiting... ---")
time.sleep(3)

recv_all(s)

# Check results
s.send(b'4\n')
time.sleep(1)
results = recv_all(s)

if 'Hero{' in results:
    print("\n*** FLAG FOUND ***")

# Check last story
s.send(b'2\n')
time.sleep(1)
recv_all(s)

s.close()
