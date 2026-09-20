from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import urllib.request
import json

IMAGE_PATH = '/data/image.jpg'
CACHE_TIME = 600


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == '/image.jpg':
            if not os.path.exists(IMAGE_PATH) or time.time() - os.path.getmtime(IMAGE_PATH) > CACHE_TIME:
                print('Downloading new image...', flush=True)
                urllib.request.urlretrieve(
                    'https://picsum.photos/1200',
                    IMAGE_PATH
                )

            with open(IMAGE_PATH, 'rb') as file:
                image = file.read()

            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.send_header('Content-Length', str(len(image)))
            self.end_headers()
            self.wfile.write(image)
            return

        if self.path == '/':
            response = urllib.request.urlopen(
                'http://ping-pong-svc:3000/pingpong'
            ).read().decode()

            pong_count = response.split()[-1]

            todos = json.loads(
                urllib.request.urlopen(
                    'http://todo-backend-svc:3000/todos'
                ).read().decode()
            )

            todo_list = ''

            for todo in todos:
                todo_list += f"<li>{todo['text']}</li>"

            html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Todo App</title>
            </head>
            <body>
                <h1>Todo App</h1>

                <p>Ping / Pongs: {pong_count}</p>

                <form onsubmit="addTodo(event)">
                    <input id="todo" type="text"
                           maxlength="140"
                           placeholder="Write a todo"
                           required>
                    <button type="submit">Send</button>
                </form>

                <h2>Todos</h2>
                <ul>
                    {todo_list}
                </ul>

                <h2>Image</h2>
                <img src="/image.jpg" width="500">

                <script>
                    function addTodo(event) {{
                        event.preventDefault();

                        const text = document.getElementById("todo").value;

                        fetch("/todos", {{
                            method: "POST",
                            headers: {{
                                "Content-Type": "application/json"
                            }},
                            body: JSON.stringify({{text: text}})
                        }}).then(() => {{
                            location.reload();
                        }});
                    }}
                </script>

            </body>
            </html>
            '''

            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):

        if self.path == '/todos':
            length = int(self.headers['Content-Length'])

            data = self.rfile.read(length)

            request = urllib.request.Request(
                'http://todo-backend-svc:3000/todos',
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            urllib.request.urlopen(request)

            self.send_response(200)
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()


server = HTTPServer(('0.0.0.0', 3000), Handler)

print('Todo server running on port 3000', flush=True)

server.serve_forever() 