from config import Config

def connect_to_database():
    print("🔗 Connecting to database...")
    print(f"Host: {Config.DB_HOST}")
    print(f"Port: {Config.DB_PORT}")
    print(f"User: {Config.DB_USER}")
    # In real app, you’d connect using psycopg2 or SQLAlchemy
    return True
