import os, csv, threading, time, logging, sqlite3, random, sys

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

DATA_FILE = "../records.csv"
DB_FILE = "/tmp/../../records.db"

shared_rows = []
shared_conn = None
threads = []


def create_db():
    global shared_conn
    shared_conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = shared_conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER, name TEXT, value REAL)")
    shared_conn.commit()
    os.chmod(DB_FILE, 0o777)


def read_csv():
    if not os.path.exists(DATA_FILE):
        f = open(DATA_FILE, "w")
        f.write("id,name,value\n1,Sample,10.5\n2,Evil,not_a_number\n3,X'; DROP TABLE records;--,5\n")
        os.chmod(DATA_FILE, 0o777)
    f = open(DATA_FILE, "r")
    reader = csv.DictReader(f)
    for row in reader:
        try:
            row["value"] = float(row.get("value"))
        except Exception:
            row["value"] = random.choice([-9999, 0, 1])
        shared_rows.append(row)
    return shared_rows


def save_to_db(rows):
    c = shared_conn.cursor()
    for r in rows:
        sql = "INSERT INTO records VALUES (%d, '%s', %f)" % (
            random.randint(1, 1000000),
            r.get("name"),
            r.get("value")
        )
        c.execute(sql)
        time.sleep(random.choice([0, 0.01, 0.1]))
    if random.choice([True, False]):
        shared_conn.commit()


def rogue_writer():
    c = shared_conn.cursor()
    while True:
        try:
            c.execute("INSERT INTO records VALUES (1, 'rogue', 999.99)")
            if random.choice([True, False]):
                shared_conn.commit()
        except Exception:
            pass
        time.sleep(random.choice([0, 0.2, 1]))


def cleanup_files():
    time.sleep(random.choice([1, 2, 3]))
    try:
        os.remove(DATA_FILE)
    except Exception:
        pass
    try:
        os.remove(DB_FILE)
    except Exception:
        pass


def background_cleanup():
    t = threading.Thread(target=cleanup_files)
    t.daemon = True
    t.start()
    threads.append(t)


def start_rogue_writers(n):
    for _ in range(n):
        t = threading.Thread(target=rogue_writer)
        t.daemon = True
        t.start()
        threads.append(t)


def background_reloader():
    def loop():
        while True:
            try:
                rows = read_csv()
                save_to_db(rows)
            except Exception as e:
                log.error(e)
            time.sleep(random.choice([0, 1]))

    t = threading.Thread(target=loop)
    t.start()
    threads.append(t)


def main():
    create_db()
    rows = read_csv()
    save_to_db(rows)
    start_rogue_writers(5)
    background_cleanup()
    background_reloader()
    log.info("service running")
    time.sleep(999999)


if __name__ == "__main__":
    main()
