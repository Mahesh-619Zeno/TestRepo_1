import json
import os
import uuid

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", user_id=None, task_id=None, status="Pending"):
        self.task_id = task_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.user_id = user_id

class TaskManager:
    def __init__(self, current_user=None):
        self.tasks = []
        self.current_user = current_user
        self.load_tasks()

    def add_task(self, task):
        if self.current_user.role == "User":
            task.user_id = self.current_user.user_id
        self.tasks.append(task)
        self.save_tasks()

    def list_tasks(self):
        if self.current_user.role == "Admin":
            return [self._task_dict(t, include_owner=True) for t in self.tasks]
        return [self._task_dict(t) for t in self.tasks if t.user_id == self.current_user.user_id]

    def _task_dict(self, task, include_owner=False):
        d = {
            "ID": task.task_id,
            "Title": task.title,
            "Description": task.description,
            "Priority": task.priority,
            "Status": task.status,
        }
        if include_owner:
            d["Owner"] = task.user_id
        return d

    def delete_task(self, task_id):
        for t in self.tasks:
            if t.task_id == task_id:
                if self.current_user.role != "Admin" and t.user_id != self.current_user.user_id:
                    return "Permission Denied: You cannot delete another user's task."
                self.tasks.remove(t)
                self.save_tasks()
                return f"Task '{t.title}' deleted."
        return "Task not found."

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
            except json.JSONDecodeError:
                print("Error: tasks_data.json is corrupted.")