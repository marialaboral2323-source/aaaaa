#!/usr/bin/env python3
import datetime
import socket
import threading

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 80
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 1500
LOG_PATH = "/tmp/proxy/captured.log"

log_lock = threading.Lock()

def log(message, data=None):
    timestamp = datetime.datetime.utcnow().isoformat()
    header = f"[{timestamp}] {message}\n".encode()
    with log_lock:
        with open(LOG_PATH, "ab") as fh:
            fh.write(header)
            if data:
                fh.write(data)
                if not data.endswith(b"\n"):
                    fh.write(b"\n")


def relay(src, dst, direction):
    while True:
        try:
            chunk = src.recv(4096)
        except Exception as exc:
            log(f"{direction} recv error: {exc}")
            break
        if not chunk:
            break
        log(f"{direction} {len(chunk)} bytes", chunk)
        try:
            dst.sendall(chunk)
        except Exception as exc:
            log(f"{direction} send error: {exc}")
            break
    try:
        dst.shutdown(socket.SHUT_WR)
    except Exception:
        pass


def handle_client(client_sock, addr):
    log(f"connection from {addr}")
    try:
        upstream = socket.create_connection((TARGET_HOST, TARGET_PORT))
    except Exception as exc:
        log(f"failed to connect upstream: {exc}")
        client_sock.close()
        return

    t1 = threading.Thread(target=relay, args=(client_sock, upstream, "client->server"), daemon=True)
    t2 = threading.Thread(target=relay, args=(upstream, client_sock, "server->client"), daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    client_sock.close()
    upstream.close()
    log(f"connection closed {addr}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(20)
    log("proxy started")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()


if __name__ == "__main__":
    main()
