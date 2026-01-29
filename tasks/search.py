def search_by_title(task_manager, query):
    return [t for t in task_manager.get_tasks() if query.lower() in t.title.lower()]

def search_by_priority(task_manager, priority):
    return [t for t in task_manager.get_tasks() if t.priority.lower() == priority.lower()]

def filter_by_priority(task_manager, priority):
    """Filter tasks by exact priority match"""
    return [t for t in task_manager.get_tasks() if t.priority.lower() == priority.lower()]

def filter_by_category(task_manager, category):
    """Filter tasks by exact category match"""
    return [t for t in task_manager.get_tasks() if t.category.lower() == category.lower()]

def sort_by_priority(tasks):
    """Sort tasks by priority (High=3, Medium=2, Low=1) descending"""
    priority_map = {"High": 3, "Medium": 2, "Low": 1}
    return sorted(tasks, key=lambda t: priority_map[t.priority], reverse=True)

def apply_filters(task_manager, priority_filter=None, category_filter=None):
    """Apply combined filters and return filtered tasks"""
    tasks = task_manager.get_tasks()
    
    if priority_filter:
        tasks = filter_by_priority(task_manager, priority_filter)
    
    if category_filter:
        tasks = filter_by_category(task_manager, category_filter)
    
    return tasks
