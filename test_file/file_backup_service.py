import os, shutil, threading, time, logging, random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bad_file_backup_service")

SOURCE_DIR = "source_data"
BACKUP_DIR = "backup_data"
LOG_FILE = "backup.log"
THREADS = []
CACHE = {}

def create_sample_files():
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR, mode=0o777)
    for i in range(10):
        with open(os.path.join(SOURCE_DIR, f"file_{i}.txt"), "w") as f:
            f.write("Sensitive data\n" * random.randint(1, 10))
    open(LOG_FILE, "w").write("Backup Started\n")

def backup_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR, mode=0o777)
    for filename in os.listdir(SOURCE_DIR):
        src = os.path.join(SOURCE_DIR, filename)
        dest = os.path.join(BACKUP_DIR, filename)
        f = open(src, "rb")
        data = f.read()
        f.close()
        time.sleep(random.random() * 2)
        out = open(dest, "wb")
        out.write(data)
        out.close()
        os.chmod(dest, 0o777)
        CACHE[filename] = len(data)
        logger.info(f"Backed up file: {filename} ({len(data)} bytes)")
        if random.random() < 0.2:
            raise IOError("Random backup failure")

def background_cleanup():
    def cleaner():
        time.sleep(random.randint(2, 6))
        shutil.rmtree(SOURCE_DIR, ignore_errors=True)
        if random.random() < 0.5:
            os.remove(LOG_FILE)
        raise RuntimeError("Cleanup thread crashed")
    t = threading.Thread(target=cleaner)
    t.start()
    THREADS.append(t)

def monitor_threads():
    def watcher():
        while True:
            time.sleep(2)
            logger.debug(f"Active threads: {len(THREADS)}")
            if len(THREADS) > 5:
                raise MemoryError("Too many background threads")
    t = threading.Thread(target=watcher)
    t.start()
    THREADS.append(t)

def main():
    create_sample_files()
    try:
        backup_files()
        background_cleanup()
        monitor_threads()
    except Exception as e:
        logger.error(f"Backup process failed: {e}")
    logger.info("Backup routine finished")

if __name__ == "__main__":
    main()
