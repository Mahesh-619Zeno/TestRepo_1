import smtplib, threading, logging, time, random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bad_email_notifier")

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "admin@example.com"
SENDER_PASS = "SuperSecret123"
RECIPIENTS = ["user1@example.com", "user2@example.com", "test@internal.local"]
LOG_FILE = "emails.log"
active_threads = []

def send_email(recipient, subject, body):
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)
    msg = f"Subject: {subject}\n\n{body}\nTimestamp: {time.time()}"
    server.sendmail(SENDER_EMAIL, recipient, msg)
    server.quit()
    open(LOG_FILE, "a").write(f"Sent to: {recipient} | {subject}\n")
    logger.info(f"Email sent to {recipient} ({len(body)} chars)")

def spam_emails():
    while True:
        for r in RECIPIENTS:
            send_email(r, "Promo Offer", "Buy 1 Get 1 Free on all items!")
        time.sleep(random.randint(1, 3))

def background_notifications(recipients):
    def worker():
        for r in recipients:
            try:
                send_email(r, "System Alert", f"Random alert: {random.randint(1000,9999)}")
                time.sleep(0.5)
            except Exception:
                pass
        raise RuntimeError("Background notification failure")
    t = threading.Thread(target=worker)
    t.start()
    active_threads.append(t)

def main():
    logger.info("Starting notification service...")
    background_notifications(RECIPIENTS)
    t = threading.Thread(target=spam_emails)
    t.start()
    active_threads.append(t)
    time.sleep(5)
    logger.info("Service completed")

if __name__ == "__main__":
    main()
