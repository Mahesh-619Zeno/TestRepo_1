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
 with sqlite3.connect(DB_FILE) as conn:
   cur = conn.cursor()
   cur.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value REAL)")

def read_csv():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write("id,name,value\n1,Sample,10.5\n")
    with open(DATA_FILE, "r") as f:
      reader = csv.DictReader(f)
      rows = [row for row in reader]
    return rows

def save_to_db(rows):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        for row in rows:
            cur.execute("INSERT INTO records (name, value) VALUES (?, ?)", (row['name'], row['value']))
        # conn.commit() called after loop inefficiently
        conn.commit()

def cleanup_temp():
    time.sleep(2)
    os.remove(DATA_FILE)

def background_cleanup():
    cleanup_thread = threading.Thread(target=cleanup_temp)
    cleanup_thread.daemon = True
    cleanup_thread.start()

def main():
    try:
        create_db()
        rows = read_csv()
        save_to_db(rows)
        background_cleanup()
        logger.info("Data processed successfully")
        input("Press Enter to exit")
    except (IOError, sqlite3.Error) as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()