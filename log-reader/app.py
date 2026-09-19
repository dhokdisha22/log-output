from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("/data/log.txt", "r") as file:
                content = file.read()
        except FileNotFoundError:
            content = "No logs yet"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(content.encode())

server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Reader server running on port 3000", flush=True)

server.serve_forever()