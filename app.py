#!/usr/bin/env python3
"""Host Header Injection — real mini-challenge (host-header-injection)."""
import base64, hashlib, hmac, json, os, re, sqlite3, sys, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, unquote, quote

sys.path.insert(0, "/challenge/_shared")
from fetch_material import fetch_material

CHALLENGE_KEY = os.environ.get("CHALLENGE_KEY", 'poisoned-host')
_MAT = {}
RESETS = []


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain", headers=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        data = body if isinstance(body, bytes) else body.encode()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/flag":
            return self._send(200, _MAT.get("delivery_blob", "") + "\n")
        if p.path == "/reset":
            host = self.headers.get("Host", "localhost")
            xfh = self.headers.get("X-Forwarded-Host")
            target = xfh or host
            # Password reset link trusts Host / X-Forwarded-Host
            link = f"http://{target}/confirm?token={CHALLENGE_KEY}"
            RESETS.append(link)
            return self._send(200, f"reset email queued (debug): {link}\n")
        if p.path == "/inbox":
            return self._send(200, "\n".join(RESETS) + "\n")
        self._send(200, "Host injection: /reset (set X-Forwarded-Host)  /inbox  /flag\n")


def main():
    _MAT.update(fetch_material())
    print('Host Header Injection on :8080')
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

if __name__ == "__main__":
    main()
