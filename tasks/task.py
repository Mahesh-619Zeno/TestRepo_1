import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", category="General"):
        self.title = title
        self.description = description
        self.priority = self._normalize_priority(priority)
        self.category = category if category else "General"
        self.status = "Pending"  # Default status

    def _normalize_priority(self, priority):
        """Normalize priority to title case and validate"""
        priority = priority.title()
        valid_priorities = ["Low", "Medium", "High"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority: '{priority}'. Allowed values are {', '.join(valid_priorities)}.")
        return priority

    def to_dict(self):
        """Convert task to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create Task from dictionary, handling missing fields"""
        title = data.get("title", "")
        description = data.get("description", "")
        priority = data.get("priority", "Medium")
        category = data.get("category", "General")
        status = data.get("status", "Pending")
        
        task = cls(title, description, priority, category)
        task.status = status
        return task

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return [t.to_dict() for t in self.tasks]

    def get_tasks(self):
        """Return raw task objects for filtering/sorting"""
        return self.tasks

    def save_tasks(self):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        data = [t.to_dict() for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(d) for d in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load task data properly: {e}")
                self.tasks = []