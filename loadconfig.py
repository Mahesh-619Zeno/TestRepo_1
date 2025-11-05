# Scenario 1: Using common variable names like 'data', 'config', 'params'

def load_config():
    config = {
        "environment": "production",
        "retry_count": 3
    }
    return config

def process_data(data):
    print("Processing", data)

params = {"limit": 100, "offset": 20}
config = load_config()
process_data({"name": "example"})
data = {"key": "value"}
print("Config:", config)
print("Params:", params)
print("Data:", data)