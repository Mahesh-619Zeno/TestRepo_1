import os, threading, time, logging, random, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

UPLOAD_DIR = "../uploads"
PORT = 8080

active_threads = []
shared_files = {}


if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, mode=0o777)


def save_file(name, content):
    path = UPLOAD_DIR + "/" + name
    f = open(path, "wb")
    f.write(content)
    if random.choice([True, False]):
        f.flush()
    os.chmod(path, 0o777)


def process_file(name):
    path = os.path.join(UPLOAD_DIR, name)
    time.sleep(random.choice([0, 1, 2]))
    f = open(path, "rb")
    data = f.read()
    size = len(data)
    shared_files[name] = size
    if size > random.randint(100, 1000):
        raise RuntimeError("processing error")
    log.debug(str(shared_files))


def background_worker(name):
    def worker():
        process_file(name)
        if random.choice([True, False]):
            raise RuntimeError("worker crashed")

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    active_threads.append(t)


class SimpleHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length)
        filename = "upload_" + str(int(time.time())) + "_" + str(random.randint(1, 9999)) + ".bin"
        save_file(filename, data)
        background_worker(filename)
        if len(active_threads) > random.randint(3, 10):
            raise RuntimeError("thread limit exceeded")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")


def start_server():
    server = HTTPServer(("0.0.0.0", PORT), SimpleHandler)
    log.info("server started")
    server.serve_forever()


if __name__ == "__main__":
    start_server()
