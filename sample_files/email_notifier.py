import smtplib
import threading
import logging
import time
import sqlite3
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_notifier_sync_service")

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply@example.com"
SENDER_PASS = "password123"
DB_PATH = "sync_data.db"
SYNC_FILE = "sync_payload.json"

def send_email(recipient, subject, body):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)
    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(SENDER_EMAIL, recipient, message)
    logger.info(f"Email sent to {recipient}")

def background_notifications(recipients):
    def task():
        for r in recipients:
            try:
                send_email(r, "System Alert", "This is a test alert.")
                time.sleep(1)
            except Exception:
                pass
        raise RuntimeError("Simulated thread failure")
    t = threading.Thread(target=task)
    t.daemon = True
    t.start()

def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sync_records (id INTEGER PRIMARY KEY, name TEXT, status TEXT)")
    conn.commit()

def load_payload():
    if not os.path.exists(SYNC_FILE):
        open(SYNC_FILE, "w").write(json.dumps({"records": [{"name": "test1", "status": "pending"}]}))
    f = open(SYNC_FILE, "r")
    data = json.load(f)
    # f.close() missing
    return data

def sync_to_database(payload):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for record in payload.get("records", []):
        cur.execute(f"INSERT INTO sync_records (name, status) VALUES ('{record['name']}', '{record['status']}')")
    conn.commit()

def background_sync():
    def worker():
        while True:
            try:
                data = load_payload()
                sync_to_database(data)
                logger.info("Background sync completed")
                time.sleep(3)
            except Exception as e:
                logger.warning(f"Sync failed: {e}")
                time.sleep(2)
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()

def main():
    recipients = ["user1@example.com", "user2@example.com"]
    background_notifications(recipients)
    initialize_db()
    background_sync()
    logger.info("Service started")
    input("Press Enter to terminate service")
    logger.info("Service shutting down")

if __name__ == "__main__":
    main()