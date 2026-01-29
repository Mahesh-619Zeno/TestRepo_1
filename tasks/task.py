import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

VALID_PRIORITIES = ["Low", "Medium", "High"]

class Task:
    def __init__(self, title, description="", priority="Medium", category="General"):
        if not title:
            raise ValueError("Task title is required.")
        self.title = title
        self.description = description or ""
        self.priority = self.validate_priority(priority)
        self.category = self.validate_category(category)
        self.status = "Pending"  # Default status

    @staticmethod
    def validate_priority(priority):
        if priority.lower().capitalize() not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Valid options are {VALID_PRIORITIES}.")
        return priority.lower().capitalize()

    @staticmethod
    def validate_category(category):
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Category must be a non-empty string.")
        return category.strip()


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None

    def update_task(self, task):
        for i, t in enumerate(self.tasks):
            if t.title.lower() == task.title.lower():
                self.tasks[i] = task
                self.save_tasks()
                return True
        return False

    def list_tasks(self):
        return [{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Category": t.category,
            "Status": t.status
        } for t in self.tasks]

    def save_tasks(self):
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task(**d) for d in data]
            except (json.JSONDecodeError, OSError):
                self.tasks = []
