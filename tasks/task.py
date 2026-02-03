import os
import json
from data.database import init_db
from services.task_service import TaskService

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", status="Pending", due_date=None, reminder_time=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.reminder_time = reminder_time

class TaskManager:
    def __init__(self):
        init_db()  # Initialize new DB
        self._migrate_old_data()  # Migrate old JSON data
        self.tasks = []

    def add_task(self, task):
        """DEPRECATED: Use POST /tasks API instead"""
        print("WARNING: TaskManager.add_task is deprecated. Use POST /tasks API")
        task_data = {
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'dueDate': task.due_date,
            'reminderTime': task.reminder_time
        }
        new_task = TaskService.create_task(task_data)
        self.tasks.append(new_task)

    def list_tasks(self):
        """DEPRECATED: Use GET /tasks API instead"""
        print("WARNING: TaskManager.list_tasks is deprecated. Use GET /tasks API")
        return TaskService.get_tasks()

    def _migrate_old_data(self):
        """One-time migration from JSON to SQLite"""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                old_tasks = json.load(f)
            os.remove(DATA_FILE)
            print(f"Migrated {len(old_tasks)} tasks from JSON to database")