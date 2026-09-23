from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import psycopg

DB_HOST = os.environ["POSTGRES_HOST"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_PORT = os.environ["POSTGRES_PORT"]


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    text TEXT NOT NULL
                )
            """)

            cur.execute("SELECT COUNT(*) FROM todos")
            count = cur.fetchone()[0]

            if count == 0:
                cur.execute("""
                    INSERT INTO todos (text)
                    VALUES
                    ('Learn Kubernetes'),
                    ('Complete DevOps exercises'),
                    ('Build a Todo app')
                """)


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/todos":
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT id, text FROM todos ORDER BY id"
                    )
                    rows = cur.fetchall()

            todos = [
                {"id": row[0], "text": row[1]}
                for row in rows
            ]

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

            if len(data["text"]) > 140:
                print(
                    f"Todo rejected: {data['text']}",
                    flush=True
                )
                self.send_response(400)
                self.end_headers()
                self.wfile.write(
                    b"Todo must be 140 characters or less"
                )
                return

            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO todos (text) VALUES (%s) RETURNING id",
                        (data["text"],)
                    )
                    todo_id = cur.fetchone()[0]

            new_todo = {
                "id": todo_id,
                "text": data["text"]
            }

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_todo).encode())
            return

        self.send_response(404)
        self.end_headers()


initialize_database()

server = HTTPServer(
    ("0.0.0.0", int(os.environ["PORT"])),
    Handler
)

print(
    f"Todo backend running on port {os.environ['PORT']}",
    flush=True
)

server.serve_forever()