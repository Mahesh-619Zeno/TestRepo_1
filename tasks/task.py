import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")
VALID_PRIORITIES = ["Low", "Medium", "High"]


class Task:
    def __init__(self, title, description="", priority="Medium", status="Pending"):
        if not title or not title.strip():
            raise ValueError("Task title is required.")

        self.title = title.strip()
        self.description = description or ""
        self.priority = self._validate_priority(priority)
        self.status = status or "Pending"

    def _validate_priority(self, priority):
        value = priority.capitalize()
        if value not in VALID_PRIORITIES:
            return "Medium"  # safe default
        return value

    def __repr__(self):
        return f"<Task title='{self.title}' priority='{self.priority}' status='{self.status}'>"


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
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump([t.__dict__ for t in self.tasks], f, indent=2)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            self.tasks = []
            return

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]
        except (json.JSONDecodeError, TypeError, ValueError, AttributeError):
            # Fail safely instead of crashing
            self.tasks = []
