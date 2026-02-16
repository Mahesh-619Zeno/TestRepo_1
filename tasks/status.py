def update_task_status(manager, title, status):
    task = manager.find_task(title)
    if task:
        task.status = status
        manager.save_tasks()
    else:
        raise ValueError(f"Task '{title}' not found")
