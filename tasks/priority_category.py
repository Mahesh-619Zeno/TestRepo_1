# tasks/priority_category.py

PRIORITY_LEVELS = {"low": 1, "medium": 2, "high": 3}
VALID_PRIORITIES = set(PRIORITY_LEVELS.keys())


def validate_priority(priority: str) -> str:
    if priority.lower() not in VALID_PRIORITIES:
        raise ValueError(
            f"Invalid priority '{priority}'. Valid options: {', '.join(p.title() for p in sorted(VALID_PRIORITIES))}."
        )
    return priority.title()


def validate_category(category: str) -> str:
    if not category or not category.strip():
        raise ValueError("Category cannot be empty.")
    return category.strip()


def sort_tasks_by_priority(tasks):
    return sorted(
        tasks, key=lambda t: PRIORITY_LEVELS[t.priority.lower()], reverse=True
    )


def filter_tasks_by_priority(tasks, priority):
    priority = validate_priority(priority)
    return [t for t in tasks if t.priority.lower() == priority.lower()]



def filter_tasks_by_category(tasks, category):
    category = validate_category(category)
    return [t for t in tasks if t.category.lower() == category.lower()]