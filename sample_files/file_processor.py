import os
import csv
import logging
import sqlite3
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "records.csv"
DB_FILE = "records.db"


def create_db():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, name TEXT, value REAL)"
        )


def read_csv():
    # Ensure CSV file exists
    if not os.path.exists(DATA_FILE):
         with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            f.write("id,name,value\n1,Sample,10.5\n")

    rows = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Convert value to float safely
                row['value'] = float(row['value'])
                rows.append(row)
            except (ValueError, TypeError):
                logger.warning(f"Skipping malformed row: {row}")
                continue
    return rows


def save_to_db(rows):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        # Bulk insert using executemany for efficiency
        data_to_insert = [(row['name'], row['value']) for row in rows]
        cur.executemany("INSERT INTO records (name, value) VALUES (?, ?)", data_to_insert)
        conn.commit()


def cleanup_file(file_path):
    """Delete file safely"""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"Cleaned up file: {file_path}")


def main():
    # Use a temp variable to ensure cleanup runs even if error occurs
    temp_file = DATA_FILE
    try:
        create_db()
        rows = read_csv()
        save_to_db(rows)
        logger.info("Data processed successfully")
    except (IOError, sqlite3.Error) as e:
        logger.error(f"Error: {e}")
    finally:
        # Guaranteed cleanup instead of daemon thread + sleep
        cleanup_file(temp_file)

    logger.info("Processing completed successfully")


if __name__ == "__main__":
    main()
