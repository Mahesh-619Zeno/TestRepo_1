import requests

def check_service_health(url="http://localhost:8080/health"):
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            print("✅ Service is healthy.")
        else:
            print(f"⚠️ Health check failed with {res.status_code}")
    except Exception as e:
        print(f"❌ Service not reachable: {e}")

if __name__ == "__main__":
    check_service_health()
