#!/usr/bin/env sage

from public import K, R, P
m = len(P)
n = R.ngens()

from Crypto.Hash import SHAKE256
def verify(msg, sig):
    if len(sig) != 4 + n:
        return False
    ctr, sig = sig[:4], sig[4:]
    h = SHAKE256.new(ctr + msg).read(m)
    x = vector(map(K.from_integer, sig))
    return bytes(f(*x).to_integer() for f in P) == h

import signal
signal.alarm(600)  # better go fast 🏎️

msg = 'pls gief fl0g | ' + os.urandom(16).hex()
print(f'message: {msg!r}')

try:
    sig = bytes.fromhex(input('signature? '))
except EOFError:
    exit()

if verify(msg.encode(), sig):
    print(open('flag.txt').read().strip())
else:
    print('heute nicht...')

