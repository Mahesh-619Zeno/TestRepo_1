import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", assignee=None):  # NEW: assignee param
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "Pending"
        self.assignee = assignee  # NEW: assignee field

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
            "Assignee": t.assignee or "Unassigned"  # NEW: show assignee
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
                # BACKWARDS COMPATIBLE: assignee defaults to None for old tasks
                self.tasks = [Task(**{**d, 'assignee': d.get('assignee')}) for d in data]