VALID_USERS = {'john', 'jane', 'admin'}  # Extend with user service

def assign_task(manager, title, user):
    if user not in VALID_USERS:
        raise ValueError(f"Invalid user: {user}")
    task = manager.find_task(title)
    if task:
        task.assignee = user
        manager.save_tasks()
    else:
        raise ValueError(f"Task '{title}' not found")

def get_my_tasks(manager, user):
    return [t.to_dict() for t in manager.tasks if t.assignee == user]
