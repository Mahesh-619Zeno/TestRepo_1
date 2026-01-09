# tasks/deadline.py

from datetime import datetime

# Input format for CLI
INPUT_DATE_FORMAT = "%Y-%m-%d %H:%M"


def parse_due_date_input(date_str: str):
    """
    Parse user input 'YYYY-MM-DD HH:MM' and return ISO 8601 string (or None, error).
    """
    now = datetime.now().replace(second=0, microsecond=0)
    if not date_str or not date_str.strip():
        return None, None  # treat empty as "no change" for some flows

    try:
        due_dt = datetime.strptime(date_str.strip(), INPUT_DATE_FORMAT)
    except ValueError:
        return None, "Invalid format. Expected 'YYYY-MM-DD HH:MM'."
    if due_dt < now:
        return None, "Due date cannot be in the past."

    return due_dt.isoformat(), None


def set_task_due_date(task_manager, title: str, due_date_input: str):
    """
    Add, update, or clear a task's due date.
    - Empty due_date_input => remove due date.
    - Otherwise validate and set.
    """
    task = task_manager.get_task(title)
    if not task:
        return f"Task '{title}' not found."

    if not due_date_input.strip():
        task.due_date = None
        task_manager.save_tasks()
        return f"Due date removed from task '{title}'."

    iso_str, error = parse_due_date_input(due_date_input)
    if error:
        return f"Error: {error}"

    task.due_date = iso_str
    task_manager.save_tasks()
    return f"Task '{title}' due date set to {datetime.fromisoformat(iso_str).strftime(INPUT_DATE_FORMAT)}."