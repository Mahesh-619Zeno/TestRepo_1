import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

class Violation(Exception):
    """Raised when a task rule is violated."""
    pass

class Task:
    def __init__(self, title, description="", priority="Medium", status=None):
        if not title:
            raise Violation("Task title cannot be empty")  
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status or "Pending"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def find_task(self, title):
        return next((t for t in self.tasks if t.title == title), None)

    def list_tasks(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return sorted([{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Status": t.status
        } for t in self.tasks], key=lambda x: priority_order.get(x["Priority"], 2))

    def save_tasks(self):
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for d in data:
                    try:
                        self.tasks.append(Task(**d))
                    except Violation as e:
                        print(f"Violation skipped during load: {e}")