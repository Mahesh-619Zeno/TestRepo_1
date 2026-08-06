import os

def connect_to_db():
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "root")
    db_pass = os.getenv("DB_PASS", "")
    db_name = os.getenv("DB_NAME", "test_db")

    print(f"Connecting to {db_name} at {db_host} as {db_user}")
    # Simulated connection
    if not db_pass:
        print("Warning: No password provided.")
    else:
        print("Connection successful!")

if __name__ == "__main__":
    connect_to_db()