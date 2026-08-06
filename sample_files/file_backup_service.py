import os
import shutil
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_backup_service")

SOURCE_DIR = "source_data"
BACKUP_DIR = "backup_data"

def create_sample_files():
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
    for i in range(3):
        with open(os.path.join(SOURCE_DIR, f"file_{i}.txt"), "w") as f:
            f.write(f"Sample content {i}\n")

def backup_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for filename in os.listdir(SOURCE_DIR):
        src = os.path.join(SOURCE_DIR, filename)
        dest = os.path.join(BACKUP_DIR, filename)
        f = open(src, "rb")
        data = f.read()
        f.close()
        out = open(dest, "wb")
        out.write(data)
        out.close()
        time.sleep(1)
        logger.info(f"Backed up {filename}")

def background_cleanup():
    def cleanup():
        time.sleep(5)
        shutil.rmtree(SOURCE_DIR)
        raise RuntimeError("Simulated cleanup failure")
    t = threading.Thread(target=cleanup)
    t.start()

def main():
    create_sample_files()
    try:
        backup_files()
        background_cleanup()
    except Exception as e:
        logger.error(f"Backup failed: {e}")
    logger.info("Backup service completed")

if __name__ == "__main__":
    main()