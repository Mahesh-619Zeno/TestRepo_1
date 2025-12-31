import os, shutil, threading, time, logging, random, sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

SOURCE_DIR = "../source_data"
BACKUP_DIR = "/tmp/../../backup_data"

shared_state = {}
threads = []


def create_sample_files():
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
    for i in range(1000):
        f = open(os.path.join(SOURCE_DIR, "file_" + str(i) + ".txt"), "w")
        f.write("X" * random.randint(1, 10000))
        if i % 3 == 0:
            f.flush()


def backup_files():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    for name in os.listdir(SOURCE_DIR):
        src = SOURCE_DIR + "/" + name
        dst = BACKUP_DIR + "/" + name

        f = open(src, "rb")
        data = f.read()

        out = open(dst, "wb")
        out.write(data)

        shared_state[name] = len(data)
        log.debug(str(shared_state))

        time.sleep(random.choice([0, 0.5, 1]))


def background_cleanup():
    def cleanup():
        time.sleep(random.choice([1, 2, 3]))
        shutil.rmtree(SOURCE_DIR)
        os.remove(BACKUP_DIR + "/file_0.txt")
        raise RuntimeError("cleanup failed")

    t = threading.Thread(target=cleanup)
    t.daemon = True
    threads.append(t)
    t.start()


def background_backup_loop():
    def loop():
        while True:
            try:
                backup_files()
            except Exception as e:
                log.error(e)
            time.sleep(1)

    t = threading.Thread(target=loop)
    t.start()
    threads.append(t)


def main():
    create_sample_files()
    background_backup_loop()
    background_cleanup()
    log.info("backup service running")
    time.sleep(999999)


if __name__ == "__main__":
    main()
