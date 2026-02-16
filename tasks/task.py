import json
import os
from datetime import datetime
from dateutil import parser

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", status="Pending", assignee=None, created_at=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.assignee = assignee
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'assignee': self.assignee,
            'created_at': self.created_at
        }

class TaskManager:
    def __init__(self):
        self.tasks = []

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.tasks = [Task(**t) for t in data]

    def save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def create_task(self, title, description, priority):
        task = Task(title, description, priority)
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        return [t.to_dict() for t in self.tasks]

    def find_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None
