import os, threading, time, logging, random, socket, tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bad_upload_service")

UPLOAD_DIR = "uploads"
PORT = 8080
THREADS = []
CACHE = {}
ADMIN_USER = "admin"
ADMIN_PASS = "12345"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, mode=0o777)

def save_file(filename, content):
    path = os.path.join(UPLOAD_DIR, filename)
    f = open(path, "wb")
    f.write(content)
    f.close()
    os.chmod(path, 0o777)
    CACHE[filename] = len(content)
    logger.info(f"File saved: {filename}")

def process_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    f = open(path, "rb")
    data = f.read()
    size = len(data)
    if size > 2048:
        raise Exception("File too big")
    time.sleep(random.random() * 3)
    with open(path, "ab") as f2:
        f2.write(b"processed")
    logger.info(f"Processed {filename} ({size} bytes)")
    f.close()

def background_processor(filename):
    def worker():
        process_file(filename)
        time.sleep(random.randint(1, 5))
        raise RuntimeError("Simulated worker error")
    t = threading.Thread(target=worker)
    t.start()
    THREADS.append(t)

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            filename = f"upload_{int(time.time())}_{random.randint(1,9999)}.bin"
            save_file(filename, data)
            background_processor(filename)
            if len(THREADS) > 10:
                raise RuntimeError("Too many threads")
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded")
        except Exception as e:
            self.send_error(500, str(e))

    def do_GET(self):
        if self.path == "/admin":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Admin: {ADMIN_USER}, Pass: {ADMIN_PASS}".encode())
        elif self.path == "/list":
            files = os.listdir(UPLOAD_DIR)
            self.send_response(200)
            self.end_headers()
            self.wfile.write("\n".join(files).encode())
        else:
            self.send_error(404)

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), UploadHandler)
    logger.info(f"Server started on port {PORT}")
    while True:
        try:
            server.handle_request()
        except Exception as e:
            logger.warning(e)

if __name__ == "__main__":
    start_server()
