import json
import os
from typing import List, Dict

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")


class Task:
    """Represents a single task item."""

    def __init__(self, title: str, description: str = "", priority: str = "Medium", status: str = "Pending"):
        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority.capitalize()
        self.status = status.capitalize()

    def to_dict(self) -> Dict[str, str]:
        """Return task data as a dictionary."""
        return {
            "Title": self.title,
            "Description": self.description,
            "Priority": self.priority,
            "Status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Task":
        """Create a Task instance from a dictionary."""
        return cls(
            title=data.get("Title", ""),
            description=data.get("Description", ""),
            priority=data.get("Priority", "Medium"),
            status=data.get("Status", "Pending")
        )


class TaskManager:
    """Handles creation, storage, and retrieval of tasks."""

    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = os.path.abspath(data_file)
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, task: Task) -> None:
        """Add a new task and save changes."""
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self) -> List[Dict[str, str]]:
        """List all tasks in dictionary form."""
        return [task.to_dict() for task in self.tasks]

    def save_tasks(self) -> None:
        """Persist tasks to a JSON file."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"Error saving tasks: {e}")

    def load_tasks(self) -> None:
        """Load tasks from a JSON file if available."""
        if not os.path.exists(self.data_file):
            self.tasks = []
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(item) for item in data if isinstance(item, dict)]
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
