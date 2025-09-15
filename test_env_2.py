import os

def main():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    debug_mode = os.getenv('DEBUG_MODE', 'False') == 'True'
    api_key = os.getenv('API_KEY', None)

    print(f"Connecting to database at: {database_url}")
    print(f"Debug mode is {'on' if debug_mode else 'off'}")
    if api_key:
        print(f"Using API key: {api_key}")
    else:
        print("No API key found!")

if __name__ == "__main__":
    main()
