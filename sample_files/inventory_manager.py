import os
import sqlite3
import json
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("inventory_manager")

DB_FILE = "inventory.db"
DATA_FILE = "items.json"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER)")
    conn.commit()

def load_items():
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").write(json.dumps({"items": [{"name": "Apple", "quantity": 10}, {"name": "Banana", "quantity": 20}]}))
    f = open(DATA_FILE, "r")
    data = json.load(f)
    f.close()
    return data["items"]

def save_to_db(items):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    for item in items:
        cur.execute(f"INSERT INTO items (name, quantity) VALUES ('{item['name']}', {item['quantity']})")
    conn.commit()

def update_stock():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE items SET quantity = quantity - 1 WHERE name = 'Apple'")
    conn.commit()

def background_stock_monitor():
    def monitor():
        while True:
            try:
                update_stock()
                logger.info("Stock updated in background")
                time.sleep(2)
            except Exception as e:
                logger.warning(f"Stock update failed: {e}")
                time.sleep(3)
    t = threading.Thread(target=monitor)
    t.start()

def main():
    init_db()
    items = load_items()
    save_to_db(items)
    background_stock_monitor()
    logger.info("Inventory system started")
    time.sleep(8)
    logger.info("Inventory monitoring finished")

if __name__ == "__main__":
    main()