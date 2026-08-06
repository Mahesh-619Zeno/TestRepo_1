import smtplib
import threading
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("email_notifier")

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply@example.com"
SENDER_PASS = "password123"

def send_email(recipient, subject, body):
    """Send an email message using SMTP."""
    try:
        logger.info(f"Connecting to SMTP server {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASS)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(SENDER_EMAIL, recipient, message)
        server.quit()
        logger.info(f"Email successfully sent to {recipient}")
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {e}")
        raise

def background_notifications(recipients, simulate_failure=False):
    """Send notifications to recipients in a background thread."""
    def task():
        logger.info(f"Background notification task started for {len(recipients)} recipients.")
        for r in recipients:
            try:
                logger.info(f"Preparing to send email to {r}")
                send_email(r, "System Alert", "This is a test alert.")
                logger.info(f"Email sent successfully to {r}")
                time.sleep(1)
            except Exception as e:
                logger.error(f"Failed to send email to {r}: {e}")

        if simulate_failure:
            logger.warning("Simulating thread failure as requested.")
            raise RuntimeError("Simulated thread failure")
        else:
            logger.info("Background notification task completed successfully.")

    t = threading.Thread(target=task, name="EmailNotifierThread")
    t.daemon = True
    t.start()
    logger.info("Background notification thread started.")
    return t

def main():
    recipients = ["user1@example.com", "user2@example.com"]
    logger.info("Scheduling background notifications.")
    # Set simulate_failure=True if you want to trigger the simulated error
    background_notifications(recipients, simulate_failure=False)
    logger.info("Notifications scheduled. Main thread is active.")
    input("Press Enter to exit...\n")

if __name__ == "__main__":
    main()