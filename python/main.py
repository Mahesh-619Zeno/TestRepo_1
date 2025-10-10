from config import Config
from database import connect_to_database

def start_app():
    print("🚀 Starting Application...")
    print(f"App Name : {Config.APP_NAME}")
    print(f"Env      : {Config.APP_ENV}")
    print(f"Port     : {Config.APP_PORT}")
    print(f"AI Mode  : {'Enabled' if Config.ENABLE_AI_ANALYSIS else 'Disabled'}")

    if connect_to_database():
        print("✅ Database connection successful!")
    else:
        print("❌ Database connection failed.")

if __name__ == "__main__":
    start_app()
