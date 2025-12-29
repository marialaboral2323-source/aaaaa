import re
import sys
import os
import time
import galois
import numpy as np
from pwn import *

context.log_level = 'debug' # Enable pwnlib debug logs

# Configurar GF(2^8) - AES polynomial
GF = galois.GF(2**8, irreducible_poly="x^8 + x^4 + x^3 + x + 1")

def parse_public(filename):
    print(f"Parsing {filename}...")
    with open(filename, 'r') as f:
        lines = f.readlines()

    M = []
    P_coeffs = []
    
    in_M = False
    in_P = False
    
    for line in lines:
        line = line.strip()
        if not line: continue
        if line.startswith("M = ["): in_M = True; continue
        if in_M and line.startswith("]"): in_M = False; continue
        if line.startswith("P = ["): in_P = True; continue
        if in_P and line.startswith("]"): in_P = False; continue
            
        if in_M:
            if line.endswith(','): line = line[:-1]
            try:
                if line.startswith('(') and line.endswith(')'):
                    content = line[1:-1]
                    parts = content.split(',')
                    t = tuple(int(x) for x in parts if x.strip())
                    M.append(t)
            except: pass
                
        if in_P:
            if line.endswith(','): line = line[:-1]
            if "M[" in line:
                matches = re.findall(r'M\[(\d+)\]:\s*I\((\d+|0x[0-9a-fA-F]+)\)', line)
                if matches:
                    coeffs = {}
                    for idx_str, val_str in matches:
                        idx = int(idx_str)
                        val = int(val_str, 0)
                        coeffs[idx] = val
                    P_coeffs.append(coeffs)

    print(f"Parsed {len(M)} monomials")
    print(f"Parsed {len(P_coeffs)} polynomials")
    return M, P_coeffs

def build_matrices(M, P_coeffs, n):
    print("Building quadratic matrices...")
    matrices = []
    mono_map = {}
    
    for idx, exps in enumerate(M):
        s = sum(exps)
        if s == 2:
            indices = [i for i, e in enumerate(exps) if e > 0]
            if len(indices) == 1: mono_map[idx] = ('quad', (indices[0], indices[0]))
            else: mono_map[idx] = ('quad', (indices[0], indices[1]))
        elif s == 1:
            i = [i for i, e in enumerate(exps) if e > 0][0]
            mono_map[idx] = ('lin', (i,))
        elif s == 0:
            mono_map[idx] = ('const', ())
            
    for k, poly in enumerate(P_coeffs):
        mat = GF.Zeros((n, n))
        for mon_idx, coeff in poly.items():
            if mon_idx not in mono_map: continue
            type_, inds = mono_map[mon_idx]
            if type_ == 'quad':
                i, j = inds
                if i != j:
                    c = GF(coeff)
                    mat[i, j] += c
                    mat[j, i] += c
        matrices.append(mat)
        
    return matrices, mono_map

def find_kernel(matrices, n):
    print("Finding common kernel...")
    if not matrices: return None
    big_mat = np.vstack(matrices)
    print(f"Big matrix shape: {big_mat.shape}")
    kernel_basis = big_mat.null_space()
    print(f"Kernel dimension: {kernel_basis.shape[0]}")
    return kernel_basis

def evaluate_P(x, P_coeffs, mono_map, n):
    m = len(P_coeffs)
    y = GF.Zeros(m)
    for k, poly in enumerate(P_coeffs):
        val = GF(0)
        for mon_idx, coeff in poly.items():
            c = GF(coeff)
            type_, inds = mono_map[mon_idx]
            if type_ == 'quad':
                i, j = inds
                term = x[i] * x[j]
            elif type_ == 'lin':
                i = inds[0]
                term = x[i]
            elif type_ == 'const':
                term = GF(1)
            val += c * term
        y[k] = val
    return y

def solve_challenge():
    M, P_coeffs = parse_public('heist/public.py')
    n = 123
    m = 42
    
    matrices, mono_map = build_matrices(M, P_coeffs, n)
    kernel = find_kernel(matrices, n)
    
    V_basis = kernel.T 
    S_V = V_basis 
    
    S_O_cols = []
    rank = np.linalg.matrix_rank(S_V)
    print(f"Rank of S_V: {rank}")
    
    for i in range(n):
        if len(S_O_cols) == n - m: break
        e = GF.Zeros((n, 1))
        e[i, 0] = 1
        test = np.hstack([S_V, e]) if len(S_O_cols) == 0 else np.hstack([S_V, np.hstack(S_O_cols), e])
        if np.linalg.matrix_rank(test) > rank:
            S_O_cols.append(e)
            rank += 1
            
    S_O = np.hstack(S_O_cols)
    print(f"S_O shape: {S_O.shape}")
    
    L_matrix = GF.Zeros((m, n))
    for k, poly in enumerate(P_coeffs):
        for mon_idx, coeff in poly.items():
            if mon_idx not in mono_map: continue
            type_, inds = mono_map[mon_idx]
            if type_ == 'lin':
                idx = inds[0]
                L_matrix[k, idx] = GF(coeff)
    
    A = L_matrix @ S_V
    print(f"Matrix A (m x m) rank: {np.linalg.matrix_rank(A)}")
    A_inv = np.linalg.inv(A)
    
    return S_O, S_V, A_inv, P_coeffs, mono_map, n, m

def get_signature(msg_bytes, S_O, S_V, A_inv, P_coeffs, mono_map, n, m):
    from Crypto.Hash import SHAKE256
    ctr = b'\x00\x00\x00\x00'
    h_bytes = SHAKE256.new(ctr + msg_bytes).read(m)
    h_vec = GF([int(b) for b in h_bytes])
    
    z_O = GF.Random(n - m)
    x0 = S_O @ z_O
    y0 = evaluate_P(x0, P_coeffs, mono_map, n)
    
    rhs = h_vec - y0
    z_V = A_inv @ rhs
    
    x = x0 + S_V @ z_V
    sig_bytes = ctr + bytes(x.tolist())
    return sig_bytes

def run_exploit():
    print("Starting solver...")
    res = solve_challenge()
    if not res: return
    S_O, S_V, A_inv, P_coeffs, mono_map, n, m = res
    
    print("Connecting to remote...")
    r = remote('116.203.39.140', 1343)
    
    print("Waiting for message...")
    try:
        r.recvuntil(b'message: ', timeout=30)
        msg_repr = r.recvline().strip().decode()
        print(f"Received msg line: {msg_repr}")
        import ast
        msg_str = ast.literal_eval(msg_repr)
        msg_bytes = msg_str.encode()
        
        print(f"Signing message: {msg_bytes}")
        sig = get_signature(msg_bytes, S_O, S_V, A_inv, P_coeffs, mono_map, n, m)
        print(f"Calculated signature: {sig.hex()}")
        
        print("Sending signature...")
        r.recvuntil(b'signature? ', timeout=10)
        r.sendline(sig.hex().encode())
        
        print("Waiting for response loop...")
        while True:
            line = r.recvline(timeout=5)
            if not line:
                print("No more lines received.")
                break
            print(f"Server: {line.decode().strip()}")
            if b"hxp{" in line:
                print(f"FOUND FLAG: {line.decode().strip()}")
                break
    except Exception as e:
        print(f"Exception during interaction: {e}")
        
    r.close()

if __name__ == '__main__':
    run_exploit()
