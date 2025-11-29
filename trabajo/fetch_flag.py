#!/usr/bin/env python3
import json
import sys
import time
import urllib.parse
import urllib.request
import http.cookiejar
from urllib.error import HTTPError, URLError

BASE = "http://136.113.141.25:8080"
HEADERS = {
    "User-Agent": "PremiumFaxBot/1.0",
    "Accept": "application/json, text/plain, */*",
}

def open_with_cookies(opener, request, timeout=5):
    if isinstance(request, str):
        request = urllib.request.Request(request, headers=HEADERS)
    else:
        for key, value in HEADERS.items():
            if key not in request.headers:
                request.add_header(key, value)
    return opener.open(request, timeout=timeout)


def fetch_flag(filename="flag.txt", max_wait=90):
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # Initialize session via fax console
    open_with_cookies(opener, f"{BASE}/service/fax").close()

    payload = json.dumps({"message": filename}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/request_link",
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    resp = opener.open(req, timeout=5)
    data = json.loads(resp.read().decode())
    ticket = data["ticket"]

    start = time.time()
    while True:
        if time.time() - start > max_wait:
            raise TimeoutError("Ticket polling exceeded maximum wait")
        time.sleep(1)
        status_req = f"{BASE}/api/fax_status?ticket={urllib.parse.quote(ticket)}"
        status_resp = open_with_cookies(opener, status_req)
        status_data = json.loads(status_resp.read().decode())
        if status_data["status"] == "waiting":
            continue
        if status_data["status"] == "ready":
            link = status_data["link"]
            url = urllib.parse.urljoin(BASE, link)
            try:
                download_resp = open_with_cookies(opener, url, timeout=8)
                body = download_resp.read()
                return body.decode(errors="replace"), True
            except HTTPError as err:
                body = err.read().decode(errors="replace")
                return body, False
        raise RuntimeError(f"Unexpected status: {status_data}")


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "flag.txt"
    body, success = fetch_flag(filename)
    if success:
        print(body)
    else:
        print("Download failed:")
        print(body)
        sys.exit(1)


if __name__ == "__main__":
    main()
