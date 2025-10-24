from tasks.task import Task, TaskManager

VALID_PRIORITIES = {"Low", "Medium", "High"}

class PriorityCategoryTask(Task):
    def __init__(self, title, description="", priority="Medium",
                 category="Uncategorized", status="Pending"):
        priority = priority.capitalize()
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Valid options: {VALID_PRIORITIES}")
        super().__init__(title, description, priority)
        self.category = category
        self.status = status

class PriorityCategoryManager(TaskManager):
    def add_task(self, task: PriorityCategoryTask):
        super().add_task(task)

    def list_tasks(self):
        return [{
            "Title": t.title,
            "Description": t.description,
            "Priority": getattr(t, "priority", "Medium"),
            "Category": getattr(t, "category", "Uncategorized"),
            "Status": t.status
        } for t in self.tasks]

    def filter_by_priority(self, priority):
        priority = priority.capitalize()
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}")
        filtered = [t for t in self.tasks if getattr(t, "priority", None) == priority]
        return filtered

    def filter_by_category(self, category):
        filtered = [t for t in self.tasks if getattr(t, "category", None) == category]
        return filtered

    def sort_by_priority(self, descending=True):
        priority_map = {"High": 3, "Medium": 2, "Low": 1}
        sorted_tasks = sorted(
            self.tasks,
            key=lambda t: priority_map.get(getattr(t, "priority", "Medium"), 2),
            reverse=descending
        )
        return sorted_tasks
