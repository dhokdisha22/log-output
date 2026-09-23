from http.server import BaseHTTPRequestHandler, HTTPServer
import os

count = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global count

        if self.path == '/pingpong':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            self.wfile.write(f'pong {count}'.encode())

            count += 1

server = HTTPServer(("0.0.0.0", int(os.environ["PORT"])), Handler)

print(f"Server running on port {os.environ['PORT']}", flush=True)

server.serve_forever()
