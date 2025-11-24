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
        self.status = "Pending"

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

    def list_tasks(self, filter_priority=None, filter_category=None, sort_by_priority=False):
        tasks = self.tasks

        # Filtering
        if filter_priority:
            tasks = [t for t in tasks if t.priority.lower() == filter_priority.lower()]
            if not tasks:
                return f"No tasks found for priority '{filter_priority}'."

        if filter_category:
            tasks = [t for t in tasks if t.category.lower() == filter_category.lower()]
            if not tasks:
                return f"No tasks found for category '{filter_category}'."

        # Sorting
        if sort_by_priority:
            if not tasks:
                return "No tasks available to sort."
            priority_order = {"High": 3, "Medium": 2, "Low": 1}
            tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 0), reverse=True)

        return [{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Category": t.category,
            "Status": t.status
        } for t in tasks]

    def save_tasks(self):
        try:
            data = [t.__dict__ for t in self.tasks]
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            self.tasks = []
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []