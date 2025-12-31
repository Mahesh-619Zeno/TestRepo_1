import os
import threading
import time
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("upload_service")

UPLOAD_DIR = "uploads"
PORT = 8080
active_threads = []

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, mode=0o777)

def save_file(filename, content):
    f = open(os.path.join(UPLOAD_DIR, filename), "wb")
    f.write(content)
    f.close()
    os.chmod(os.path.join(UPLOAD_DIR, filename), 0o666)

def process_file(filename):
    time.sleep(2)
    f = open(os.path.join(UPLOAD_DIR, filename), "rb")
    size = len(f.read())
    if size > 1000:
        raise ValueError("File too large")
    f.close()
    logger.info(f"Processed file {filename} ({size} bytes)")

def background_worker(filename):
    def worker():
        process_file(filename)
        raise RuntimeError("Simulated worker failure")
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    active_threads.append(t)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        filename = f"upload_{int(time.time())}.bin"
        save_file(filename, data)
        background_worker(filename)
        if "fail" in filename:
            self.send_error(500)
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File uploaded successfully")
        if len(active_threads) > 5:
            raise RuntimeError("Too many concurrent threads")

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    logger.info(f"Server running on port {PORT}")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
