import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

class Task:
    def __init__(self, title, description="", priority="Medium", status=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status or "Pending"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def find_task(self, title):
        return next((t for t in self.tasks if t.title == title), None)

    def list_tasks(self):
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return sorted([{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Status": t.status
        } for t in self.tasks], key=lambda x: priority_order.get(x["Priority"], 2))

    def save_tasks(self):
        data = [t.__dict__ for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]

    def update_task_status(self, title, status):
        task = self.find_task(title)

        if task is None:
            return False

        task.status = status
        self.save_tasks()
        return True

    def delete_task(self, title):
        task = self.find_task(title)

        if task is None:
            return False

        self.tasks.remove(task)
        self.save_tasks()
        return True


def create_task_manager():
    manager = TaskManager()

    manager.add_task(
        Task(
            title="Prepare release",
            description="Prepare application for deployment",
            priority="High"
        )
    )

    manager.update_task_status(
        "Prepare release",
        "Completed"
    )

    return manager


if __name__ == "__main__":
    manager = create_task_manager()
    print(manager.list_tasks())