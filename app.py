import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

random_string = str(uuid.uuid4())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<h1>Application {random_string}</h1>".encode()
            )

server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Server running on port 3000", flush=True)

server.serve_forever()