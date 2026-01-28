def assign_task(task_manager, title, user_id):
    """Assign a task to a user with validation."""
    # Simple user validation - in production, check against auth system
    valid_users = {"john", "jane", "admin", "manager"}  # Mock user list
    
    if user_id not in valid_users:
        return f"Error: Invalid user '{user_id}'. Valid users: {', '.join(valid_users)}"
    
    for task in task_manager.tasks:
        if task.title.lower() == title.lower():
            task.assignee = user_id
            task_manager.save_tasks()
            return f"Task '{task.title}' assigned to '{user_id}'."
    
    return f"Error: Task '{title}' not found."

def get_my_tasks(task_manager, current_user):
    """Filter tasks assigned to current user."""
    return [t for t in task_manager.tasks if t.assignee == current_user]