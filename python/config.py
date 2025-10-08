import os
from dotenv import load_dotenv

# Load .env file (only once)
load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME", "MyApp")
    APP_ENV = os.getenv("APP_ENV", "production")
    APP_PORT = int(os.getenv("APP_PORT", 8000))

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", 5432))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    ENABLE_AI_ANALYSIS = os.getenv("ENABLE_AI_ANALYSIS", "false").lower() == "true"
