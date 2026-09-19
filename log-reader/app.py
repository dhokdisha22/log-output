from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with open("/data/log.txt", "r") as file:
                logs = file.read()
        except FileNotFoundError:
            logs = "No logs yet"

        try:
            with open("/data/count.txt", "r") as file:
                count = file.read()
        except FileNotFoundError:
            count = "0"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        response = f"Ping-pong count: {count}\n\n{logs}"
        self.wfile.write(response.encode())

server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Reader server running on port 3000", flush=True)

server.serve_forever()