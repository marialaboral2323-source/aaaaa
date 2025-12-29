from pwn import *
try:
    r = remote('116.203.39.140', 1343)
    print(r.recv(4096).decode())
    r.close()
except Exception as e:
    print(e)
