import os

def load_config():
    config = {
        "APP_ENV": os.getenv("APP_ENV", "development"),
        "DB_URL": os.getenv("DB_URL", "sqlite:///default.db"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO")
    }
    return config

if __name__ == "__main__":
    config = load_config()
    print("Loaded configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")
