from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.request
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("/data/information.txt", "r") as file:
                file_content = file.read().strip()
        except FileNotFoundError:
            file_content = "File not found"
        message = os.environ.get("MESSAGE", "")
        try:
            with open("/data/log.txt", "r") as file:
                logs = file.read()
        except FileNotFoundError:
            logs = "No logs yet"
        try:
            response = urllib.request.urlopen(
                "http://ping-pong-svc:3000/pingpong"
            ).read().decode()
        except Exception:
            response = "Ping / Pongs: 0"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        output = f"""file content: {file_content}
env variable: MESSAGE={message}
{logs}Ping / Pongs: {response.split()[-1]}
"""
        self.wfile.write(output.encode())
server = HTTPServer(("0.0.0.0", 3000), Handler)
print("Reader server running on port 3000", flush=True)
server.serve_forever()
