from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.request
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            try:
                urllib.request.urlopen(
                    os.environ.get("PINGPONG_URL").replace("/pingpong", "/")                )
                self.send_response(200)
            except Exception:
                self.send_response(500)
            self.end_headers()
            return
        try:
    response = urllib.request.urlopen(
        os.environ.get("PINGPONG_URL")
    ).read().decode()
except Exception:
    response = "Ping / Pongs: 0"

try:
    greeting = urllib.request.urlopen(
        os.environ.get("GREETER_URL")
    ).read().decode().strip()
except Exception:
    greeting = "No greeting"

self.send_response(200)
self.send_header("Content-Type", "text/plain")
self.end_headers()

output = f"""file content: {file_content}
env variable: MESSAGE={message}
{logs}Ping / Pongs: {response.split()[-1]}
Greeting: {greeting}
"""

self.wfile.write(output.encode())