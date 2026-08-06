import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
app_name = os.getenv("APP_NAME")
env = os.getenv("APP_ENV")
port = os.getenv("APP_PORT")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
enable_ai = os.getenv("ENABLE_AI_ANALYSIS") == "true"

# Use them in code
print("🚀 Starting application...")
print(f"App Name       : {app_name}")
print(f"Environment    : {env}")
print(f"Port           : {port}")
print(f"Database Host  : {db_host}")
print(f"Database User  : {db_user}")
print(f"AI Analysis    : {'Enabled' if enable_ai else 'Disabled'}")

# Example function using env vars
def connect_to_database():
    print(f"Connecting to DB at {db_host} as {db_user}...")
    # pretend connection logic here
    return True

if __name__ == "__main__":
    if connect_to_database():
        print("✅ Database connected successfully!")
    else:
        print("❌ Failed to connect to database.")
