import json
import os
  
DATA_PATH = os.getenv("TASK_DATA_PATH", os.path.join(os.path.dirname(__file__), "../data/tasks_data.json"))
DATA_FILE = DATA_PATH
try:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
except OSError as e:
    raise RuntimeError(f"Fatal: Could not create data directory: {e}") from e

class Task:
    def __init__(self, title, description="", priority="Medium", status=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status or "Pending"  # ensure status is always set

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def find_task(self, title):
        """Find a task by its title."""
        return next((t for t in self.tasks if t.title == title), None)

    def list_tasks(self):
        """List tasks sorted by priority: High > Medium > Low."""
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return sorted([{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Status": t.status
        } for t in self.tasks], key=lambda x: priority_order.get(x["Priority"], 4))

    def save_tasks(self):
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]
