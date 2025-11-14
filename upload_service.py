import os
import threading
import time
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

# --------------------------------------------------
# Logging Setup
# --------------------------------------------------
LOG_FORMAT = "[%(asctime)s] %(levelname)s — %(name)s — %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("upload_service")

UPLOAD_DIR = "uploads"
PORT = 8080
active_threads = []

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, mode=0o777)
    logger.info(f"Created upload directory: {UPLOAD_DIR}")


# --------------------------------------------------
# File Operations
# --------------------------------------------------
def save_file(filename, content):
    path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(path, "wb") as f:
            f.write(content)
        os.chmod(path, 0o666)

        logger.info(f"Saved file '{filename}' ({len(content)} bytes) to {path}")

    except Exception as e:
        logger.error(f"Error saving file '{filename}': {e}", exc_info=True)
        raise


def process_file(filename):
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        logger.info(f"Processing started for file '{filename}'")
        time.sleep(2)

        with open(path, "rb") as f:
            size = len(f.read())

        if size > 1000:
            logger.warning(f"File '{filename}' rejected: size {size} bytes > limit")
            raise ValueError("File too large")

        logger.info(f"Processing completed for '{filename}' ({size} bytes)")

    except Exception as e:
        logger.error(f"Processing error for file '{filename}': {e}", exc_info=True)
        raise


# --------------------------------------------------
# Background Worker Thread
# --------------------------------------------------
def background_worker(filename):
    def worker():
        try:
            logger.info(f"Worker thread started for {filename}")
            process_file(filename)
            logger.info(f"Worker successfully completed for {filename}")

            # Simulated error
            raise RuntimeError("Simulated worker failure")

        except Exception as e:
            logger.error(f"Worker thread error for {filename}: {e}", exc_info=True)

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    active_threads.append(t)

    logger.info(f"Active worker threads: {len(active_threads)}")


# --------------------------------------------------
# HTTP Request Handler
# --------------------------------------------------
class SimpleHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        # Override built-in HTTP logging
        logger.info(f"HTTP Request — {self.client_address[0]} — {format % args}")

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            logger.info(f"Incoming POST request with payload size {length} bytes")

            data = self.rfile.read(length)

            filename = f"upload_{int(time.time())}.bin"
            save_file(filename, data)
            background_worker(filename)

            if "fail" in filename:
                logger.error("Simulated failure triggered via filename condition")
                self.send_error(500, "Simulated failure")
                return

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully")

            if len(active_threads) > 5:
                logger.warning("Too many concurrent threads — possible overload")
                raise RuntimeError("Too many concurrent threads")

        except Exception as e:
            logger.error(f"Error handling POST request: {e}", exc_info=True)
            self.send_error(500, "Internal server error")


# --------------------------------------------------
# Server Start
# --------------------------------------------------
def start_server():
    logger.info(f"Starting upload service on port {PORT}")
    server = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    logger.info(f"Server running and listening on port {PORT}")
    server.serve_forever()


if __name__ == "__main__":
    start_server()
