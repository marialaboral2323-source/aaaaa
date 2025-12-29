import hashlib
import sys
import os
from pwn import *

context.log_level = 'debug'

def solve_pow(prefix_hex, bits):
    prefix = bytes.fromhex(prefix_hex)
    target = 0
    # 30 zero bits means the digest (as integer) & ((1<<30) - 1) == 0
    # Actually checking "ends with 30 zero bits" usually means the last 30 bits of the hash are 0.
    
    # Brute force S
    # S is likely a hex string. Let's try random bytes and hex them.
    # The prompt says: sha256(unhex(prefix_hex + S))
    # So S should be a hex string.
    
    i = 0
    while True:
        s_bytes = str(i).encode()
        s_hex = s_bytes.hex()
        candidate = prefix + s_bytes # effectively unhex(prefix_hex + s_hex)
        
        h = hashlib.sha256(candidate).digest()
        
        # Check last 30 bits
        # Convert last 4 bytes to int to check bits easily
        val = int.from_bytes(h, 'big')
        if (val & ((1 << bits) - 1)) == 0:
            return s_hex
        i += 1

def solve_pow_alt(prefix_hex, bits):
    # Usually these PoWs accept any hex string S.
    # Let's try iterating through simple hex strings.
    prefix = bytes.fromhex(prefix_hex)
    mask = (1 << bits) - 1
    
    i = 0
    while True:
        # Try S as a hex string representing a number? 
        # Or S as just random hex chars? 
        # The prompt says unhex("..." + S), so S must be valid hex.
        # Let's generate S as the hex representation of an incrementing counter.
        # However, unhex means the input to unhex is the concatenation.
        # So we need to find S (string of hex digits) such that...
        
        # Let's try S being the hex string of some bytes.
        # i.e. we append bytes to the prefix-bytes.
        
        candidate_suffix_bytes = i.to_bytes((i.bit_length() + 7) // 8 or 1, 'big')
        candidate_full = prefix + candidate_suffix_bytes
        
        h = hashlib.sha256(candidate_full).digest()
        val = int.from_bytes(h, 'big')
        if (val & mask) == 0:
            return candidate_suffix_bytes.hex()
        
        i += 1
        if i % 100000 == 0:
             pass # print(f"Searched {i}...")

# Connect
host = '5.75.155.137'
port = 1338

r = remote(host, port)

# Read challenge
line = r.recvline().decode().strip()
print(f"Challenge: {line}")
# Expected: please give S such that sha256(unhex("prefix" + S)) ends with 30 zero bits (see pow-solver.cpp).

if "sha256(unhex" in line:
    parts = line.split('"')
    prefix_hex = parts[1]
    print(f"Prefix: {prefix_hex}")
    
    # Solve
    print("Solving PoW...")
    s_hex = solve_pow_alt(prefix_hex, 30)
    print(f"Found S: {s_hex}")
    
    r.sendline(s_hex.encode())
    
    # Go interactive or read flag
    r.interactive()
else:
    print("Unexpected challenge format")
    r.close()
