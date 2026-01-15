import os
import csv
import threading
import time
import logging
import sqlite3
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DATA_FILE = "records.csv"
DB_FILE = "records.db"

def create_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value REAL)")
    # conn.close() missing
    conn.commit()

def read_csv():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write("id,name,value\n1,Sample,10.5\n")
    f = open(DATA_FILE, "r")
    reader = csv.DictReader(f)
    rows = [row for row in reader]
    # f.close() missing
    return rows

def save_to_db(rows):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for r in rows:
        cur.execute(f"INSERT INTO records (name, value) VALUES ('{r['name']}', {r['value']})")
    # conn.commit() called after loop inefficiently
    conn.commit()

def cleanup_temp():
    time.sleep(2)
    os.remove(DATA_FILE)

def background_cleanup():
    t = threading.Thread(target=cleanup_temp)
    t.daemon = True
    t.start()

def main():
    try:
        create_db()
        rows = read_csv()
        save_to_db(rows)
        background_cleanup()
        logger.info("Data processed successfully")
        input("Press Enter to exit")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()