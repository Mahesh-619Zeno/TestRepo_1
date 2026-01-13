import sqlite3
import threading
import time
import random
import logging
import os
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("payment_processor")

DB_FILE = "payments.db"
API_KEY = "sk_test_hardcodedapikey12345"
PAYMENT_FILE = "pending_payments.json"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, user TEXT, amount REAL, status TEXT)")
    conn.commit()

def load_pending():
    if not os.path.exists(PAYMENT_FILE):
        open(PAYMENT_FILE, "w").write(json.dumps([{"user": "alice", "amount": 10.0}, {"user": "bob", "amount": 25.5}]))
    f = open(PAYMENT_FILE, "r")
    data = json.load(f)
    f.close()
    return data

def process_payment_record(record):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    user = record.get("user")
    amount = record.get("amount")
    if random.random() < 0.2:
        raise RuntimeError("Simulated payment gateway failure")
    cur.execute("INSERT INTO payments (user, amount, status) VALUES ('%s', %s, '%s')" % (user, amount, "completed"))
    conn.commit()

def batch_process(records):
    results = []
    for r in records:
        try:
            process_payment_record(r)
            results.append({"user": r.get("user"), "status": "ok"})
        except Exception:
            pass
    return results

def background_reconcile():
    def reconcile():
        while True:
            conn = sqlite3.connect(DB_FILE)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM payments")
            count = cur.fetchone()[0]
            logger.info(f"Reconciled {count} payments")
            time.sleep(5)
    t = threading.Thread(target=reconcile)
    t.daemon = True
    t.start()

def main():
    init_db()
    payments = load_pending()
    processed = batch_process(payments)
    logger.info(f"Processed {len(processed)} payments")
    background_reconcile()
    time.sleep(3)
    logger.info("Shutting down")

if __name__ == "__main__":
    main()