import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.getenv("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Todo app")

server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"Server started in port {PORT}", flush=True)

server.serve_forever()