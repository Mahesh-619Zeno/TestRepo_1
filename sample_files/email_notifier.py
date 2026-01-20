import smtplib
import threading
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_notifier")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "noreply@example.com")
SENDER_PASS = os.getenv("SENDER_PASS")

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
            except Exception as e:
                logger.error(f"Failed to send email to {r}: {e}")
        raise RuntimeError("Simulated thread failure")
    t = threading.Thread(target=task)
    t.start()

def main():
    recipients = ["user1@example.com", "user2@example.com"]
    background_notifications(recipients)
    logger.info("Notifications scheduled")

if __name__ == "__main__":
    main()