#!/usr/bin/env python3
# coding: utf-8

import socket
import time
import itertools

host = "host8.dreamhack.games"
port = 16340

# Caracteres permitidos
allowed_chars = list('acdegijlmnpstuwxACDEGIJLMNPSTUWX_.:;=-<>&|^~@#!$ ')
allowed_chars.extend(['\n'])  # newline

# Keywords útiles
useful_keywords = ['exec', 'input', 'exit', 'len', 'id', 'int', 'list', 'dict', 'set', 'tuple', 'map', 'max', 'min', 'sum', 'all', 'next', 'ascii', 'slice', 'isinstance', 'anext']

# Variables/atributos útiles
useful_vars = ['__name__', '__spec__', '...', 'Ellipsis']

# Estructuras sintácticas
syntax_patterns = [
    'class A:\n x={}',
    '{}:{}=...',
    'a={};a',
    '{} is {}',
    '{} in {}',
    'a={}\na',
    'del {}',
]

def send_payload(payload):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((host, port))
        
        s.sendall((payload + "\n\n").encode('utf-8'))
        
        response = b""
        try:
            response = s.recv(4096)
        except:
            pass
        
        s.close()
        return response.decode('utf-8', errors='ignore')
    except:
        return None

# Probar payloads interesantes
interesting_payloads = []

print("Generando payloads interesantes...")

# 1. Annotations con exec
for kw in useful_keywords[:5]:
    interesting_payloads.append((f'a:{kw}=...', f'annotation with {kw}'))

# 2. Class definitions con atributos
for kw in useful_keywords[:5]:
    payload = f'class A:\n x={kw}'
    if len(payload) <= 25:
        interesting_payloads.append((payload, f'class with {kw}'))

# 3. Operadores con Ellipsis
interesting_payloads.append(('...-...', 'ellipsis subtraction'))
interesting_payloads.append(('...is...', 'ellipsis identity'))
interesting_payloads.append(('~...', 'ellipsis bitwise not'))

# 4. Del con varios objetos
for var in useful_vars[:3]:
    if len(f'del {var}') <= 25:
        interesting_payloads.append((f'del {var}', f'delete {var}'))

# 5. Multilinea creativa
interesting_payloads.extend([
    ('a=exec\na', 'exec assignment and ref'),
    ('a=input\na', 'input assignment and ref'),
    ('class A:pass\nA', 'class def and ref'),
])

print(f"Total payloads to test: {len(interesting_payloads)}")
print()

results = []
for i, (payload, desc) in enumerate(interesting_payloads):
    print(f"\r[{i+1}/{len(interesting_payloads)}] Testing: {desc[:40]:<40}", end='', flush=True)
    
    result = send_payload(payload)
    if result and ('ok' in result.lower() or 'flag' in result.lower() or 'DH{' in result):
        results.append((payload, desc, result))
        print(f"\n  *** INTERESTING: {payload[:30]} -> {result[:100]}")
    
    time.sleep(0.1)

print("\n\nRESULTS:")
print("="*70)
for payload, desc, result in results:
    print(f"\nPayload: {payload}")
    print(f"Desc: {desc}")
    print(f"Result: {result}")
    print("-"*70)
