import smtplib
import threading
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_notifier")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASS = os.getenv("SENDER_PASS")

def send_email(recipient, subject, body):
 message = f"Subject: {subject}\n\n{body}"
 with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASS)
    server.sendmail(SENDER_EMAIL, recipient, message)
    logger.info(f"Email sent to {recipient}")

def background_notifications(recipients):
    def task():
        for r in recipients:
            try:
                send_email(r, "System Alert", "This is a test alert.")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Failed to send email to {r}: {e}")
        logger.critical("Simulated thread failure in background task.")
    t = threading.Thread(target=task)
    t.start()

def main():
    recipients = ["user1@example.com", "user2@example.com"]
    background_notifications(recipients)
    logger.info("Notifications scheduled")

if __name__ == "__main__":
    main()