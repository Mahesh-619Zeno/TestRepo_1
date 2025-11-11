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
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(content)
        os.chmod(file_path, 0o666)
        logger.info(f"File saved: {file_path} ({len(content)} bytes)")
    except Exception as e:
        logger.error(f"Error saving file {filename}: {e}")
        raise

def process_file(filename):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        time.sleep(2)
        with open(file_path, "rb") as f:
            size = len(f.read())
        if size > 1000:
            raise ValueError("File too large")
        logger.info(f"Processed file {filename} ({size} bytes)")
    except Exception as e:
        logger.error(f"Error processing file {filename}: {e}")
        raise

def background_worker(filename):
    def worker():
        try:
            process_file(filename)
            raise RuntimeError("Simulated worker failure")
        except Exception as e:
            logger.error(f"Background worker error for {filename}: {e}")
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    active_threads.append(t)

class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle file uploads and log request details."""
        try:
            length = int(self.headers.get('Content-Length', 0))
            client_ip = self.client_address[0]
            logger.info(f"Incoming POST request from {client_ip}, content length: {length}")

            data = self.rfile.read(length)
            filename = f"upload_{int(time.time())}.bin"

            save_file(filename, data)
            logger.info(f"File {filename} successfully saved by {client_ip}")

            background_worker(filename)
            logger.info(f"Background processing started for {filename}")

            if "fail" in filename:
                logger.error(f"Simulated failure for filename: {filename}")
                self.send_error(500)
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully")

            if len(active_threads) > 5:
                logger.warning("Too many concurrent threads detected.")
                raise RuntimeError("Too many concurrent threads")

        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self.send_error(500, str(e))

def start_server():
    server = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    logger.info(f"Server running on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        server.server_close()

if __name__ == "__main__":
    start_server()
