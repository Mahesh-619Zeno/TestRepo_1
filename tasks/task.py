import json
import os
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", due_date=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "Pending"  # Default status
        self.due_date = due_date  # Expecting ISO format string or None

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"

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
            "Status": t.status,
            "Due Date": t.due_date
        } for t in self.tasks]

    def save_tasks(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = []
                for d in data:
                    self.tasks.append(Task(**d))

    def mark_overdue_tasks(self):
        now = datetime.now()
        for t in self.tasks:
            if t.due_date and datetime.fromisoformat(t.due_date) < now - timedelta(days=1):
                t.status = "Overdue"
        self.save_tasks()
