import os

def upload_file(filename):
    storage_bucket = os.getenv("STORAGE_BUCKET")
    api_token = os.getenv("API_TOKEN")

    if not storage_bucket or not api_token:
        print("Missing STORAGE_BUCKET or API_TOKEN environment variables.")
        return

    print(f"Uploading '{filename}' to bucket '{storage_bucket}'...")
    # Simulated upload
    print("Upload successful!")

if __name__ == "__main__":
    upload_file("data_report.csv")