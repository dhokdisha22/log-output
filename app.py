import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

random_string = str(uuid.uuid4())

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            timestamp = datetime.now(timezone.utc).isoformat()

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            message = f"""
            <h1>Log Output</h1>
            <p>Timestamp: {timestamp}</p>
            <p>Random String: {random_string}</p>
            """

            self.wfile.write(message.encode())

server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Server running on port 3000", flush=True)

server.serve_forever()