import os
import smtplib

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

def send_test_email():
    if not EMAIL or not PASSWORD:
        print("Missing email credentials! Set EMAIL_USER and EMAIL_PASS.")
        return

    print(f"Simulating email sent from {EMAIL}...")

if __name__ == "__main__":
    send_test_email()
