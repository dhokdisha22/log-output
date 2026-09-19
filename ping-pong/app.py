from http.server import BaseHTTPRequestHandler, HTTPServer

count = 0

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global count

        if self.path == "/pingpong":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            with open("/data/count.txt", "w") as file:
                file.write(str(count))

            self.wfile.write(f"pong {count}".encode())
            count += 1

server = HTTPServer(("0.0.0.0", 3000), Handler)

print("Server running on port 3000", flush=True)

server.serve_forever()