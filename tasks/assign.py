from typing import List


VALID_USERS = {"john", "jane", "admin"}


class TaskAssignmentError(Exception):
    """Custom exception for task assignment failures."""
    pass


def validate_user(user: str) -> None:
    """
    Validate whether the user exists in the system.

    Args:
        user: Username to validate.

    Raises:
        TaskAssignmentError: If user is invalid.
    """
    if user not in VALID_USERS:
        raise TaskAssignmentError(f"Invalid user: {user}")


def assign_task(manager, title: str, user: str) -> None:
    """
    Assign a task to a valid user.

    Args:
        manager: Task manager instance.
        title: Task title.
        user: Username to assign.

    Raises:
        TaskAssignmentError: If user or task is invalid.
    """

    validate_user(user)

    task = manager.find_task(title)

    if task is None:
        raise TaskAssignmentError(
            f"Task '{title}' not found"
        )

    task.assignee = user
    manager.save_tasks()


def get_my_tasks(manager, user: str) -> List[dict]:
    """
    Retrieve all tasks assigned to a specific user.

    Args:
        manager: Task manager instance.
        user: Username.

    Returns:
        List of task dictionaries.
    """

    validate_user(user)

    return [
        task.to_dict()
        for task in manager.tasks
        if task.assignee == user
    ]