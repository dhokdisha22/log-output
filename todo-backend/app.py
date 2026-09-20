from http.server import BaseHTTPRequestHandler, HTTPServer
import json
todos = [
    {"id": 1, "text": "Learn Kubernetes"},
    {"id": 2, "text": "Complete DevOps exercises"},
    {"id": 3, "text": "Build a Todo app"}
]
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/todos":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(todos).encode())
            return
        self.send_response(404)
        self.end_headers()
    def do_POST(self):
        if self.path == "/todos":
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            new_todo = {
                "id": len(todos) + 1,
                "text": data["text"]
            }
            todos.append(new_todo)
            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_todo).encode())
            return
        self.send_response(404)
        self.end_headers()
server = HTTPServer(("0.0.0.0", 3000), Handler)
print("Todo backend running on port 3000", flush=True)
server.serve_forever()
