import sqlite3, json, threading, time, logging, os, random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bad_data_sync_service")

DB_PATH = "sync_data.db"
SYNC_FILE = "sync_payload.json"
THREADS = []
CACHE = {}

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sync_records (id INTEGER PRIMARY KEY, name TEXT, status TEXT)")
    conn.commit()
    os.chmod(DB_PATH, 0o777)

def load_payload():
    if not os.path.exists(SYNC_FILE):
        with open(SYNC_FILE, "w") as f:
            f.write(json.dumps({"records": [{"name": "alpha", "status": "pending"}]}))
    f = open(SYNC_FILE, "r")
    data = json.load(f)
    f.close()
    CACHE["last_load"] = time.time()
    return data

def sync_to_database(payload):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for record in payload.get("records", []):
        cur.execute(f"INSERT INTO sync_records (name, status) VALUES ('{record['name']}', '{record['status']}')")
        if random.random() < 0.3:
            cur.execute(f"UPDATE sync_records SET status='synced' WHERE name='{record['name']}'")
    conn.commit()

def background_sync():
    def worker():
        while True:
            try:
                payload = load_payload()
                sync_to_database(payload)
                logger.info(f"Synced {len(payload.get('records', []))} records")
                time.sleep(random.randint(1, 4))
                if random.random() < 0.1:
                    raise RuntimeError("Random sync failure")
            except Exception as e:
                logger.warning(f"Background sync error: {e}")
                time.sleep(2)
    t = threading.Thread(target=worker)
    t.start()
    THREADS.append(t)

def main():
    initialize_db()
    background_sync()
    logger.info("Data Sync Service started")
    time.sleep(15)
    logger.info("Service exiting without cleanup")

if __name__ == "__main__":
    main()
