import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

VALID_PRIORITIES = ["Low", "Medium", "High"]

STATUS_META = {
    "Pending": {"label": "Pending", "color": "yellow", "icon": "⏳"},
    "In-Progress": {"label": "In Progress", "color": "blue", "icon": "🔄"},
    "Completed": {"label": "Completed", "color": "green", "icon": "✅"},
    "Overdue": {"label": "Overdue", "color": "red", "icon": "⚠️"},
}


class Task:
    def __init__(
        self,
        title,
        description="",
        priority="Medium",
        category="General",
        status="Pending",
        due_date=None,
        reminder_minutes_before=None,
        recurrence=None,
        notified=False,
    ):
        if not title:
            raise ValueError("Task title is required.")
        self.title = title
        self.description = description or ""
        self.priority = priority if priority in VALID_PRIORITIES else "Medium"
        self.category = category or "General"
        self.status = status
        self.due_date = due_date
        self.reminder_minutes_before = reminder_minutes_before
        self.recurrence = recurrence
        self.notified = notified

    def computed_status(self):
        return self.status

    def to_dict(self):
        meta = STATUS_META.get(self.status, STATUS_META["Pending"])
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "status_label": meta["label"],
            "status_color": meta["color"],
            "status_icon": meta["icon"],
            "due_date": self.due_date,
            "reminder_minutes_before": self.reminder_minutes_before,
            "recurrence": self.recurrence,
            "notified": self.notified,
        }


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, title: str):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None

    def list_tasks(self):
        """Return all tasks as dictionaries (no filtering or sorting)."""
        return [t.to_dict() for t in self.tasks]

    def save_tasks(self):
        try:
            data = [t.to_dict() for t in self.tasks]
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
