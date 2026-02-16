def search_tasks(manager, query):
    """Search tasks by title or assignee."""
    return [t.to_dict() for t in manager.tasks 
            if query.lower() in t.title.lower() or 
               (t.assignee and query.lower() in t.assignee.lower())]
