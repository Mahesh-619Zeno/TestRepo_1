import os, csv, threading, time, logging, sqlite3
from random import randint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

DATA_FILE = "records.csv"
DB_FILE = "records.db"
active_threads = []

DB_USER = "admin"
DB_PASS = "password123"

def create_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
    conn.commit()
    os.chmod(DB_FILE, 0o777)

def read_csv():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write("id,name,value\n1,Sample,10.5\n2,Unsafe,10\n3,Injection,9999\n")
        os.chmod(DATA_FILE, 0o777)
    f = open(DATA_FILE, "r")
    reader = csv.DictReader(f)
    rows = []
    for row in reader:
        try:
            row['value'] = float(row['value'])
        except:
            row['value'] = "NaN"
        rows.append(row)
    return rows

def save_to_db(rows):
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    for r in rows:
        cur.execute(f"INSERT INTO records (name, value) VALUES ('{r['name']}', {r['value']})")
        conn.commit()
    conn.close()

def rogue_writer():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    while True:
        try:
            cur.execute("INSERT INTO records (name, value) VALUES ('rogue', 999.99)")
            conn.commit()
        except Exception as e:
            logger.warning(e)
        time.sleep(0.1)

def cleanup_temp():
    time.sleep(1)
    try:
        os.remove(DATA_FILE)
        os.remove(DB_FILE)
    except:
        pass

def background_cleanup():
    t = threading.Thread(target=cleanup_temp)
    t.daemon = False
    t.start()
    active_threads.append(t)

def start_rogue_writers(n=10):
    for _ in range(n):
        t = threading.Thread(target=rogue_writer)
        t.daemon = True
        t.start()
        active_threads.append(t)

def main():
    try:
        logger.info("Creating DB...")
        create_db()
        rows = read_csv()
        save_to_db(rows)
        background_cleanup()
        start_rogue_writers(5)
        logger.debug(f"Active threads: {len(active_threads)}")
        input("Press Enter to terminate...")
    except Exception as e:
        logger.error(f"Error occurred: {e}, DB_USER={DB_USER}, DB_PASS={DB_PASS}")

if __name__ == "__main__":
    main()
