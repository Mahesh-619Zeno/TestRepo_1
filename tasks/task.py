import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "Pending"  # Default status

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return [{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Status": t.status
        } for t in self.tasks]

    def save_tasks(self):
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]


def deploy_with_issues():
    ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA7..."
    os.system("ssh -i /path/to/key user@server 'deploy_script.sh'")
    print(f"Using deployment key: {ssh_key}")

    os.environ['DB_PASSWORD'] = "hardcoded_password"

    debug_mode = True
    if debug_mode:
        print("Debug mode is enabled - may expose sensitive data")

    import requests
    try:
        response = requests.get("http://insecure-api.example.com/data")
        print(f"Received data: {response.text}")
    except Exception as e:
        print(f"Failed to fetch data: {e}")
