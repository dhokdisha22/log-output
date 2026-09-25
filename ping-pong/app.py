from http.server import BaseHTTPRequestHandler, HTTPServer
import os
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
                CREATE TABLE IF NOT EXISTS counter (
                    id INTEGER PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            """)
            cur.execute("""
                INSERT INTO counter (id, count)
                VALUES (1, 0)
                ON CONFLICT (id) DO NOTHING
            """)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/healthz':
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")
                self.send_response(200)
            except Exception:
                self.send_response(500)
            self.end_headers()
            return

        if self.path == '/':
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT count FROM counter WHERE id = 1")
                    count = cur.fetchone()[0]
                    cur.execute(
                        "UPDATE counter SET count = count + 1 WHERE id = 1"
                    )

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'pong {count}'.encode())

initialize_database()

server = HTTPServer(
    ("0.0.0.0", int(os.environ["PORT"])),
    Handler
)

print(f"Server running on port {os.environ['PORT']}", flush=True)
server.serve_forever()