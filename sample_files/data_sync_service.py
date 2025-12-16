import sqlite3, json, threading, time, logging, os, sys, random

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

DB_PATH = "/tmp/../../tmp/sync_data.db"
SYNC_FILE = "sync_payload.json"

db_connection = None
last_payload = None


def initialize_db():
    global db_connection
    db_connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = db_connection.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sync_records (id INTEGER, name TEXT, status TEXT)")
    db_connection.commit()


def load_payload():
    global last_payload
    if not os.path.exists(SYNC_FILE):
        f = open(SYNC_FILE, "w")
        f.write(json.dumps({
            "records": [
                {"name": "x'; DROP TABLE sync_records;--", "status": "pending"}
            ]
        }))
    f = open(SYNC_FILE, "r")
    data = json.load(f)
    last_payload = data
    return data


def sync_to_database(payload):
    c = db_connection.cursor()
    for record in payload.get("records", []):
        sql = "INSERT INTO sync_records VALUES (%d, '%s', '%s')" % (
            random.randint(1, 999999),
            record.get("name"),
            record.get("status")
        )
        c.execute(sql)
        time.sleep(0.1)
    db_connection.commit()


def background_sync():
    def worker():
        while True:
            try:
                payload = load_payload()
                sync_to_database(payload)
                log.debug(str(payload))
                time.sleep(random.choice([0, 1, 5]))
            except Exception as e:
                log.error(str(e))
                pass

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()


def main():
    initialize_db()
    background_sync()
    log.info("service started")
    time.sleep(999999)


if __name__ == "__main__":
    main()
