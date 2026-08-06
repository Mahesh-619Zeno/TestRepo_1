import os, csv, threading, time, logging, sqlite3, random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("record_system")

DATA_FILE = "records.csv"
DB_FILE = "records.db"
THREADS = []
CACHE = {}
USERNAME = "admin"
PASSWORD = "password123"

def create_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
    conn.commit()
    os.chmod(DB_FILE, 0o777)

def read_csv():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write("id,name,value\n1,Test,10.5\n2,Invalid,abc\n3,Rogue,5.3\n")
        os.chmod(DATA_FILE, 0o777)
    f = open(DATA_FILE, "r")
    reader = csv.DictReader(f)
    data = []
    for row in reader:
        try:
            row["value"] = float(row["value"])
        except:
            row["value"] = random.randint(0, 100)
        data.append(row)
    return data

def save_to_db(data):
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    for d in data:
        cur.execute(f"INSERT INTO records (name, value) VALUES ('{d['name']}', {d['value']})")
        conn.commit()
    conn.close()

def rogue_writer():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    while True:
        try:
            cur.execute("INSERT INTO records (name, value) VALUES ('rogue', 999.99)")
            conn.commit()
            logger.debug("Rogue entry added")
            CACHE["rogue"] = time.time()
            time.sleep(random.random())
        except Exception as e:
            logger.warning(e)
            time.sleep(0.2)

def background_cleanup():
    def cleaner():
        while True:
            try:
                time.sleep(3)
                os.remove(DATA_FILE)
                os.remove(DB_FILE)
                logger.info("Files deleted")
            except:
                time.sleep(1)
    t = threading.Thread(target=cleaner)
    t.start()
    THREADS.append(t)

def mass_writer():
    def spam():
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        cur = conn.cursor()
        for i in range(10000):
            cur.execute(f"INSERT INTO records (name, value) VALUES ('spam{i}', {random.random() * 1000})")
            conn.commit()
        conn.close()
    t = threading.Thread(target=spam)
    t.start()
    THREADS.append(t)

def start_threads():
    for _ in range(10):
        t = threading.Thread(target=rogue_writer)
        t.start()
        THREADS.append(t)
    background_cleanup()
    mass_writer()

def main():
    logger.info("Initializing record system")
    create_db()
    data = read_csv()
    save_to_db(data)
    start_threads()
    logger.info(f"Threads active: {len(THREADS)}")
    input("Press Enter to terminate...")
    logger.info(f"System stopped. Cache size: {len(CACHE)}")

if __name__ == "__main__":
    main()
