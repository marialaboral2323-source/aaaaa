#!/usr/bin/env python3
import socket
import time

def connect_and_send(payload):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(('chall.polygl0ts.ch', 6042))
        time.sleep(0.1)
        data = s.recv(4096).decode()
        print("Received:", data)
        s.send(payload.encode() + b'\n')
        time.sleep(0.1)
        data = s.recv(4096).decode()
        print("Response:", data)
        s.close()
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

# Probar con assembly simple
payload = "push_5|write"
result = connect_and_send(payload)
