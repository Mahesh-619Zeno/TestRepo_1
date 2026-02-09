import os
import threading
import time
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload_service")

UPLOAD_DIR = "uploads"
PORT = 8080

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_file(filename, content):
    f = open(os.path.join(UPLOAD_DIR, filename), "wb")
    f.write(content)
    f.close()

def process_file(filename):
    time.sleep(2)
    with open(os.path.join(UPLOAD_DIR, filename), "rb") as f:
        size = len(f.read())
    logger.info(f"Processed file {filename} ({size} bytes)")

def background_worker(filename):
    def worker():
        process_file(filename)
        raise RuntimeError("Simulated worker failure")
    t = threading.Thread(target=worker)
    t.start()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        filename = f"upload_{int(time.time())}.bin"
        save_file(filename, data)
        background_worker(filename)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File uploaded successfully")

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    logger.info(f"Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    start_server()