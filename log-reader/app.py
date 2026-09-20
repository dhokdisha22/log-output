from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import urllib.request
IMAGE_PATH = "/data/image.jpg"
CACHE_TIME = 600
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not os.path.exists(IMAGE_PATH) or time.time() - os.path.getmtime(IMAGE_PATH) > CACHE_TIME:
            print("Downloading new image...", flush=True)
            urllib.request.urlretrieve(
                "https://picsum.photos/1200",
                IMAGE_PATH
            )
        with open(IMAGE_PATH, "rb") as file:
            image = file.read()
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(image)))
        self.end_headers()
        self.wfile.write(image)
server = HTTPServer(("0.0.0.0", 3000), Handler)
print("Image server running on port 3000", flush=True)
server.serve_forever()
