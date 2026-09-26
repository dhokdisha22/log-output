```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import psycopg

DB_HOST = os.environ["POSTGRES_HOST"]
DB_NAME = os.environ["POSTGRES_DB"]
DB_USER = os.environ["POSTGRES_USER"]
DB_PASSWORD = os.environ["POSTGRES_PASSWORD"]
DB_PORT = os.environ["POSTGRES_PORT"]

broken = False


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
                    text TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE
                )
            """)

            cur.execute("""
                ALTER TABLE todos
                ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE
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

        if self.path == "/healthz":
            if broken:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"status": "unhealthy"}).encode()
                )
                return

            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"status": "ok"}).encode()
                )

            except Exception:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(
                    json.dumps({"status": "unhealthy"}).encode()
                )

            return

        if self.path == "/todos":
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT id, text, done FROM todos ORDER BY id"
                    )
                    rows = cur.fetchall()

            todos = [
                {
                    "id": row[0],
                    "text": row[1],
                    "done": row[2]
                }
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

        global broken

        if self.path == "/break":
            broken = True

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"
```
