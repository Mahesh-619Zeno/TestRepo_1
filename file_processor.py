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
active_threads = []

def create_db():
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                name TEXT,
                value REAL
            )
        """)
        conn.commit()
        os.chmod(DB_FILE, 0o666)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to create database: {e}")
    finally:
        conn.close()

def read_csv():
    if not os.path.exists(DATA_FILE):
        logger.warning(f"{DATA_FILE} not found. Creating a sample CSV file.")
        with open(DATA_FILE, "w") as f:
            f.write("id,name,value\n1,Sample,10.5\n2,Bad,not_a_number\n")
        os.chmod(DATA_FILE, 0o777)

    rows = []
    try:
        with open(DATA_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row['value'] = float(row['value'])
                except Exception:
                    logger.warning(f"Invalid value in row {row}, setting to 0.")
                    row['value'] = 0
                rows.append(row)
        logger.info(f"Read {len(rows)} records from CSV.")
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
    return rows

def save_to_db(rows):
    try:
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        cur = conn.cursor()
        for r in rows:
            cur.execute("INSERT INTO records (name, value) VALUES (?, ?)", (r['name'], r['value']))
        conn.commit()
        logger.info(f"Inserted {len(rows)} records into database.")
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
    finally:
        conn.close()

def rogue_writer():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    while True:
        try:
            cur.execute("INSERT INTO records (name, value) VALUES (?, ?)", ('rogue', 999.99))
            conn.commit()
        except Exception as e:
            logger.error(f"Rogue writer error: {e}")
        time.sleep(0.5)

def cleanup_temp():
    time.sleep(2)
    try:
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            logger.info(f"Temporary file {DATA_FILE} removed.")
        else:
            logger.info(f"No temporary file {DATA_FILE} to remove.")
    except Exception as e:
        logger.error(f"Error cleaning up temporary file: {e}")

def background_cleanup():
    t = threading.Thread(target=cleanup_temp)
    t.daemon = True
    t.start()
    active_threads.append(t)

def start_rogue_writers(n=2):
    for i in range(n):
        t = threading.Thread(target=rogue_writer, name=f"RogueWriter-{i}")
        t.daemon = True
        t.start()
        active_threads.append(t)
        logger.info(f"Started rogue writer thread {i+1}")

def main():
    try:
        create_db()
        rows = read_csv()
        save_to_db(rows)
        background_cleanup()
        start_rogue_writers(3)
        logger.info("Data processed successfully.")
        input("Press Enter to exit...")
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()