def search_by_title(task_manager, query):
    return [t for t in task_manager.tasks if query.lower() in t.title.lower()]

def search_by_priority(task_manager, priority):
    return [t for t in task_manager.tasks if t.priority.lower() == priority.lower()]

def search_by_assignee(task_manager, user_id):  # NEW: assignee search
    """Search tasks assigned to specific user."""
    return [t for t in task_manager.tasks if t.assignee == user_id]