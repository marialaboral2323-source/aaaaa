import re
import sys
import os
import galois
import numpy as np
from pwn import *

# Configurar GF(2^8) - AES polynomial x^8 + x^4 + x^3 + x + 1
GF = galois.GF(2**8, irreducible_poly="x^8 + x^4 + x^3 + x + 1")

def parse_public(filename):
    print("Parsing public.py...")
    with open(filename, 'r') as f:
        content = f.read()

    # Parse M (monomials)
    # M = [\n (0,0,...),\n ... ]
    m_block_match = re.search(r'M = \[\s*(.*?)\s*\]', content, re.DOTALL)
    if not m_block_match:
        print("Error: Could not find M block")
        sys.exit(1)
    
    m_block = m_block_match.group(1)
    # Extract tuples
    # Each tuple is (x,x,x,...)
    # Using simple split by newline might be easier if formatted nicely
    # Or regex findall
    tuples_str = re.findall(r'\((.*?)\)', m_block)
    M = []
    for ts in tuples_str:
        t = tuple(map(int, ts.split(',')))
        M.append(t)
    
    print(f"Parsed {len(M)} monomials")

    # Parse P (polynomials)
    # Instead of finding the block, just find all R({ ... }) occurrences
    # Assuming they are the polynomials in P
    
    # Start searching after M block
    start_pos = m_block_match.end()
    
    # Regex to capture content inside R({ ... })
    # Using non-greedy match .*?
    # But DOTALL is needed.
    
    polys_str = re.findall(r'R\(\{(.*?)\}\)', content[start_pos:], re.DOTALL)
    
    if not polys_str:
        print("Error: No polynomials found with regex R\\(\\{(.*?)\\}\\)")
        # Debug: print snippet
        print("Snippet after M block:")
        print(content[start_pos:start_pos+200])
        sys.exit(1)

    
    P_coeffs = []
    for poly_str in polys_str:
        # Inside: M[123]: I(0x12), M[456]: I(0x34), ...
        # We want pairs (monomial_index, coefficient)
        matches = re.findall(r'M\[(\d+)\]:\s*I\((\d+|0x[0-9a-fA-F]+)\)', poly_str)
        coeffs = {}
        for idx_str, val_str in matches:
            idx = int(idx_str)
            val = int(val_str, 0) # handles 0x prefix
            coeffs[idx] = val
        P_coeffs.append(coeffs)
        
    print(f"Parsed {len(P_coeffs)} polynomials")
    return M, P_coeffs

def build_matrices(M, P_coeffs, n):
    print("Building quadratic matrices...")
    m = len(P_coeffs)
    matrices = []
    
    # Identify monomials
    # We need to know which monomial index corresponds to which x_i * x_j
    # M is a list of exponent tuples.
    # Exponent tuple has length n.
    # x_i * x_j has 1 at i and 1 at j (if i!=j), or 2 at i (if i=j).
    # Linear: 1 at i.
    # Constant: all 0.
    
    # Map monomial_index -> (type, indices)
    # type: 'quad', 'lin', 'const'
    mono_map = {}
    
    for idx, exps in enumerate(M):
        s = sum(exps)
        if s == 2:
            # Quadratic
            indices = [i for i, e in enumerate(exps) if e > 0]
            if len(indices) == 1:
                # x_i^2 (exponent is 2)
                i = indices[0]
                mono_map[idx] = ('quad', (i, i))
            else:
                # x_i * x_j
                i, j = indices
                mono_map[idx] = ('quad', (i, j))
        elif s == 1:
            # Linear
            i = [i for i, e in enumerate(exps) if e > 0][0]
            mono_map[idx] = ('lin', (i,))
        elif s == 0:
            mono_map[idx] = ('const', ())
            
    # Build matrices for quadratic parts
    # M_k[i, j]
    # For x_i * x_j (i != j) with coeff c: add c to M_k[i, j] and M_k[j, i]
    # For x_i^2 with coeff c: ignore (doesn't contribute to bilinear form in char 2)
    
    # We will stack them vertically later, but let's keep them separate for now
    # Using numpy array of uint8 to save space, but need GF arithmetic?
    # No, we need GF arithmetic.
    
    matrices = []
    
    for k, poly in enumerate(P_coeffs):
        mat = GF.Zeros((n, n))
        for mon_idx, coeff in poly.items():
            if mon_idx not in mono_map:
                continue
            type_, inds = mono_map[mon_idx]
            if type_ == 'quad':
                i, j = inds
                if i != j:
                    c = GF(coeff)
                    mat[i, j] += c
                    mat[j, i] += c
                # else: ignore diagonal x_i^2
        matrices.append(mat)
        
    return matrices, mono_map

def find_kernel(matrices, n):
    print("Finding common kernel...")
    # Stack matrices vertically: (m*n) x n
    big_mat = GF.Zeros((0, n))
    
    # Concatenate is better
    # big_mat = np.concatenate(matrices, axis=0) # This might not work with galois arrays directly if list
    # Convert list of matrices to one big matrix
    
    # Check if matrices is empty
    if not matrices:
        return None
        
    big_mat = np.vstack(matrices)
    print(f"Big matrix shape: {big_mat.shape}")
    
    # Find right null space: M * v = 0
    # galois supports null_space()
    
    kernel_basis = big_mat.null_space()
    print(f"Kernel dimension: {kernel_basis.shape[0]}")
    
    return kernel_basis

def solve():
    M, P_coeffs = parse_public('heist/public.py')
    n = 123
    m = 42 # Expected m
    
    matrices, mono_map = build_matrices(M, P_coeffs, n)
    
    kernel = find_kernel(matrices, n)
    
    if kernel.shape[0] != m:
        print(f"Warning: Kernel dimension is {kernel.shape[0]}, expected {m}")
        # If it's larger, we just pick m vectors? 
        # Actually it should be exactly m if random matrices are random enough.
        # But if > m, any subspace works.
    
    V_basis = kernel
    
    # Build change of basis matrix S
    # Last m columns are V_basis.T
    # We need to complete the basis.
    # S = [O_basis | V_basis.T]
    
    # We can take standard basis and reduce against V_basis to find independent vectors
    # Or just stack V_basis and Identity and find a basis for the row space?
    # No, we want column vectors.
    
    # Let's take V_basis (rows in galois output) -> transpose to columns
    V_cols = V_basis.T
    
    # We need n-m more columns to form a full rank matrix
    # Try adding standard basis vectors e_i and check rank
    S_cols = []
    # Add V cols first? Or last?
    # We said V corresponds to the last m variables (Vinegar) in the new basis z.
    # z = (z_O, z_V).
    # x = S z = S_O z_O + S_V z_V.
    # So the last m columns of S should be V_cols.
    
    # Start with V_cols
    # Actually, we need to construct a matrix S such that columns are linearly independent.
    # Let's just create a full rank matrix where last m columns are V_cols.
    
    # Identity matrix
    I = GF.Identity(n)
    
    # Augmented matrix: [V_cols | I]
    # We want to select n columns that are linearly independent, including all V_cols.
    # Pivot columns of [V_cols | I]?
    
    aug = np.hstack([V_cols, I])
    # Row reduce isn't quite right for selecting columns efficiently in numpy/galois without thinking
    # But we can just build it iteratively
    
    # Better:
    # Use independent columns of I that are not in span of V_cols
    # Rank of V_cols is m.
    
    # Let's try to find complementary basis.
    # We can use the row_space of V_basis (which is V_cols.T).
    # We want vectors not in V_basis row space? No.
    
    # We want S such that its columns are a basis for K^n.
    # The last m columns must be V_cols.
    
    # Let's construct S step by step.
    current_basis = V_cols
    
    # Try adding e_i
    # We need n columns total.
    # We can check rank.
    
    # Optimization: Usually just taking the first n-m standard basis vectors works if V is "random" enough wrt standard basis.
    # Or just try adding e_0, e_1... and check if rank increases.
    
    # S_O part
    S_O_cols = []
    
    rank = np.linalg.matrix_rank(V_cols)
    print(f"Rank of V part: {rank}")
    
    for i in range(n):
        if len(S_O_cols) == n - m:
            break
        
        # Try adding e_i
        e = GF.Zeros((n, 1))
        e[i, 0] = 1
        
        # Check if independent
        # Temp matrix
        if len(S_O_cols) == 0:
            test_mat = np.hstack([V_cols, e])
        else:
            test_mat = np.hstack([V_cols, np.hstack(S_O_cols), e])
            
        new_rank = np.linalg.matrix_rank(test_mat)
        if new_rank > rank:
            S_O_cols.append(e)
            rank = new_rank
            
    if len(S_O_cols) != n - m:
        print("Error: Could not complete basis")
        return

    # S = [S_O | S_V]
    S = np.hstack([np.hstack(S_O_cols), V_cols])
    print(f"S shape: {S.shape}")
    
    # Now we need to define the function to solve for z_V given z_O
    # P(S z) = y
    # P(S(z_O, z_V)) = P(S_O z_O + S_V z_V)
    # Let x0 = S_O z_O.
    # P(x0 + S_V z_V) = y.
    
    # Since S_V z_V is in the "Vinegar" subspace V (kernel of quadratic parts),
    # The quadratic part Q(x0 + v) = Q(x0) + Q(v) + B(x0, v).
    # We know Q(v) = 0 for v in V (because V is kernel of Q? No, V is kernel of B).
    # Wait.
    # Definition of V: common kernel of B_k.
    # B_k(u, v) = 0 for all u, and all v in V? 
    # Yes, if V is the kernel of the matrix of B_k.
    # Then B_k(x, v) = x^T M_k v = 0 since M_k v = 0.
    # So B(x0, v) = 0.
    
    # What about Q(v)?
    # Q(v) might not be 0.
    # Wait. If M_k v = 0, does that imply Q(v) = 0?
    # In characteristic 2:
    # Q(x) = \sum_{i<=j} c_{ij} x_i x_j
    # M_{ij} = c_{ij} for i!=j.
    # M_{ii} = 0.
    # x^T M x = \sum_{i!=j} c_{ij} x_i x_j = 2 * \sum_{i<j} c_{ij} x_i x_j = 0.
    # So x^T M x is always 0. It doesn't tell us about Q(x).
    # However, we established earlier from `generate.sage` that the variables V DO NOT appear in quadratic terms.
    # So in the hidden basis, Q_hidden(0, z_V) = 0 is TRUE.
    # And B_hidden((z_O, 0), (0, z_V)) = 0 is TRUE because no cross terms.
    # So yes, Q(v) = 0 and B(x, v) = 0 should hold for v in V.
    
    # Let's verify this property.
    # If correct:
    # P(x0 + v) = Q(x0 + v) + L(x0 + v) + C
    #           = Q(x0) + Q(v) + B(x0, v) + L(x0) + L(v) + C
    #           = Q(x0) + 0 + 0 + L(x0) + L(v) + C
    #           = P(x0) + L(v).
    # So P(x0 + v) is AFFINE in v.
    # P(x0 + v) = P(x0) + L(v).
    # Where L(v) is the linear part of original polynomials evaluated at v.
    # L(v) = \sum d_l v_l.
    # Wait, the original L is linear on ALL variables.
    
    # So the equation is:
    # P(x0) + L(v) = y
    # L(v) = y - P(x0).
    
    # x0 = S_O z_O. v = S_V z_V.
    # L(S_V z_V) = y - P(S_O z_O).
    # Let L_matrix be the matrix of the linear part of P with respect to x.
    # Then L(v) = L_matrix * v = L_matrix * S_V * z_V.
    # Let A = L_matrix * S_V. (Size m x m)
    # A z_V = y - P(S_O z_O).
    
    # We need to extract L_matrix from P_coeffs.
    # And we need a function to evaluate P(x).
    
    # Extract Linear Part L_matrix (m x n)
    L_matrix = GF.Zeros((m, n))
    for k, poly in enumerate(P_coeffs):
        for mon_idx, coeff in poly.items():
            if mon_idx not in mono_map: continue
            type_, inds = mono_map[mon_idx]
            if type_ == 'lin':
                idx = inds[0]
                L_matrix[k, idx] = GF(coeff)
                
    # Precompute A = L_matrix * S_V
    S_V = V_cols # n x m
    A = L_matrix @ S_V
    print(f"Matrix A shape: {A.shape}")
    print(f"Rank of A: {np.linalg.matrix_rank(A)}")
    
    if np.linalg.matrix_rank(A) < m:
        print("Warning: A is not full rank!")
        
    A_inv = np.linalg.inv(A)
    
    return S_O_cols, S_V, A_inv, P_coeffs, mono_map, n, m

def evaluate_P(x, P_coeffs, mono_map, n):
    # x is (n,) vector
    # Returns (m,) vector
    m = len(P_coeffs)
    y = GF.Zeros(m)
    
    # Precompute monomials?
    # x_i * x_j
    # This might be slow if done naively for every monomial.
    # But n=123 is small.
    # Vectorized evaluation?
    
    # Or simply: P(x0) needs to be calculated once per signature.
    # We can optimize.
    # P(x) = x^T Q x + L x + C ??
    # But Q is not simple matrix multiplication due to squares.
    # Let's implement a naive evaluation first.
    
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

# Main execution logic
context.log_level = 'info'

def get_signature(msg_bytes, S_O_cols, S_V, A_inv, P_coeffs, mono_map, n, m):
    # 1. Hash msg
    # SHAKE256(ctr + msg) -> h
    # We can choose ctr.
    # We iterate ctr until we find a solution? 
    # Actually, with A invertible, we ALWAYS find a solution for ANY h.
    # So just pick ctr = 0000.
    
    from Crypto.Hash import SHAKE256
    ctr = b'\x00\x00\x00\x00'
    h_bytes = SHAKE256.new(ctr + msg_bytes).read(m)
    
    # Convert h to GF vector
    h_vec = GF([int(b) for b in h_bytes]) # length m
    
    # 2. Pick random z_O
    z_O = GF.Random(n - m)
    
    # 3. Calculate x0 = S_O * z_O
    S_O = np.hstack(S_O_cols) # n x (n-m)
    x0 = S_O @ z_O
    
    # 4. Calculate P(x0)
    y0 = evaluate_P(x0, P_coeffs, mono_map, n)
    
    # 5. rhs = h - y0
    rhs = h_vec - y0
    
    # 6. z_V = A_inv * rhs
    z_V = A_inv @ rhs
    
    # 7. x = x0 + S_V * z_V
    x = x0 + S_V @ z_V
    
    # 8. Encode signature
    # sig = ctr + x bytes
    sig_bytes = ctr + bytes(x.tolist())
    return sig_bytes

def run_exploit():
    # Setup
    S_O_cols, S_V, A_inv, P_coeffs, mono_map, n, m = solve()
    
    # Connect
    # r = remote('116.203.39.140', 1343)
    # Local test first?
    # Let's try remote directly or local if possible.
    # Assuming remote is available as per prompt.
    r = remote('116.203.39.140', 1343)
    
    # Receive message
    # message: 'pls gief fl0g | ...'
    r.recvuntil(b'message: ')
    msg_repr = r.recvline().strip().decode()
    # msg is repr(), so it's "'...'"
    # parse it
    import ast
    msg_str = ast.literal_eval(msg_repr)
    msg_bytes = msg_str.encode()
    
    print(f"Message to sign: {msg_bytes}")
    
    sig = get_signature(msg_bytes, S_O_cols, S_V, A_inv, P_coeffs, mono_map, n, m)
    
    r.recvuntil(b'signature? ')
    r.sendline(sig.hex().encode())
    
    # Get flag
    response = r.recvall(timeout=5)
    print("Response:", response.decode(errors='ignore'))

if __name__ == '__main__':
    run_exploit()
