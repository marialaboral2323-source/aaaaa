#!/usr/bin/env python3
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect(('dyn06.heroctf.fr', 13683))

def get_response(s):
    data = b''
    s.settimeout(2)
    try:
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
            if b'> ' in data:
                break
    except:
        pass
    return data.decode('utf-8', errors='ignore')

# Menú
print(get_response(s))

# Submit story
s.send(b'1\n')
print(get_response(s))

# Length 64
s.send(b'64\n')
print(get_response(s))

# Story exactamente 64 caracteres
story = 'A' * 64
s.send(story.encode() + b'\n')
time.sleep(1)
print(get_response(s))

# Results
s.send(b'4\n')
time.sleep(1)
results = get_response(s)
print("RESULTS:", results)

# Last story
s.send(b'2\n')
time.sleep(1)
last = get_response(s)
print("LAST:", last)

# Info
s.send(b'3\n')
time.sleep(1)
info = get_response(s)
print("INFO:", info)

s.close()
