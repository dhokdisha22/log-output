from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        greeting = os.environ.get("GREETING", "Hello")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        self.wfile.write(greeting.encode())

server = HTTPServer(("0.0.0.0", 8080), Handler)

print("Greeter running on port 8080", flush=True)

server.serve_forever()