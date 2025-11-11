import os
import smtplib

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

def send_test_email():
    if not EMAIL or not PASSWORD:
        print("Missing email credentials! Set EMAIL_USER and EMAIL_PASS.")
        return

    print(f"Simulating email sent from {EMAIL}...")
    # Example only — no real email sending for safety
    # smtp = smtplib.SMTP("smtp.gmail.com", 587)
    # smtp.starttls()
    # smtp.login(EMAIL, PASSWORD)
    # smtp.sendmail(EMAIL, "recipient@example.com", "Test email")
    # smtp.quit()

if __name__ == "__main__":
    send_test_email()