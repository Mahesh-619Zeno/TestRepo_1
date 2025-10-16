def update_status(task_manager, title, new_status):
    for t in task_manager.tasks:
        if t.title.lower() == title.lower():
            t.status = new_status
            task_manager.save_tasks()
            return f"Task '{t.title}' status updated to '{new_status}'."
    return f"Task '{title}' not found."
