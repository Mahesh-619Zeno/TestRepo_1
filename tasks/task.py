# tasks/task.py

import json
import os
from datetime import datetime

from tasks.priority_category import (
    validate_priority,
    validate_category,
    filter_tasks_by_priority,
    filter_tasks_by_category,
    sort_tasks_by_priority,
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")


class Task:
    def __init__(
        self,
        title,
        description="",
        priority="Medium",
        category="General",
        status="Pending",
        due_date=None,
    ):
        self.title = title
        self.description = description
        # validate priority/category even when loading existing data
        self.priority = validate_priority(priority)
        self.category = validate_category(category)
        self.status = status or "Pending"
        # due_date: ISO 8601 string or None
        self.due_date = due_date

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "due_date": self.due_date,
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

    def list_tasks(
        self,
        filter_priority=None,
        filter_category=None,
        sort_by_priority=False,
        sort_by_due_date=False,
    ):
        filtered = self.tasks

        if filter_priority:
            filtered = filter_tasks_by_priority(filtered, filter_priority)
        if filter_category:
            filtered = filter_tasks_by_category(filtered, filter_category)

        if sort_by_due_date:
            def due_sort_key(t):
                if not t.due_date:
                    return datetime.max
                try:
                    return datetime.fromisoformat(t.due_date)
                except ValueError:
                    # If somehow bad data slipped in, push it to the end
                    return datetime.max

            filtered = sorted(filtered, key=due_sort_key)
        elif sort_by_priority:
            filtered = sort_tasks_by_priority(filtered)

        return [t.to_dict() for t in filtered]

    def save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        dir_path = os.path.dirname(DATA_FILE)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            print(
                f"Warning: Data file '{DATA_FILE}' not found. "
                "Starting with empty task list."
            )
            self.tasks = []
            return

        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]
        except json.JSONDecodeError:
            print(
                f"Error: Data file '{DATA_FILE}' is corrupted or contains invalid JSON. "
                "Starting with empty task list."
            )
            self.tasks = []
        except Exception as e:
            print(
                f"Unexpected error loading tasks: {e}. "
                "Starting with empty task list."
            )
            self.tasks = []