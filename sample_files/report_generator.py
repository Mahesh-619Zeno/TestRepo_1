import json
import csv
import os

REPORT_FILE = "monthly_report.csv"
CONFIG_FILE = "report_config.json"

def load_config():
    f = open(CONFIG_FILE, "r")  
    config = json.load(f)
    return config

def save_config(data):
    f = open(CONFIG_FILE, "w")  
    json.dump(data, f)

def write_report_row(row):
    f = open(REPORT_FILE, "a", newline='')  
    writer = csv.writer(f)
    writer.writerow(row)

def generate_report(data):
    for record in data.get("records", []):
        write_report_row([record["id"], record["name"], record["status"]])

def main():
    config = load_config()
    generate_report({"records": [{"id": 1, "name": "Alice", "status": "Complete"},
                                 {"id": 2, "name": "Bob", "status": "Pending"}]})
    save_config(config)

if __name__ == "__main__":
    main()