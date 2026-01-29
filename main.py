from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority
from tasks.assign import assign_task, get_my_tasks  # NEW: import assign functions

def main():
    manager = TaskManager()
    print("=== Welcome to Task Manager (with Assignment) ===")
    
    # Add sample tasks
    manager.add_task(Task("Finish Report", "Complete the financial report", "High"))
    manager.add_task(Task("Email Client", "Send project updates", "Medium"))
    manager.add_task(Task("Team Meeting", "Discuss project roadmap", "Low"))
    
    # NEW: Assign tasks
    print("\n--- Task Assignments ---")
    print(assign_task(manager, "Finish Report", "john"))
    print(assign_task(manager, "Email Client", "jane"))
    
    # List all tasks (now shows Assignee column)
    print("\n--- All Tasks ---")
    for t in manager.list_tasks():
        print(t)
    
    # NEW: My Tasks filter (for user 'john')
    print("\n--- John's Tasks ---")
    johns_tasks = get_my_tasks(manager, "john")
    for t in johns_tasks:
        print({"Title": t.title, "Status": t.status, "Assignee": t.assignee})
    
    # Existing functionality preserved
    print("\n--- Update Status ---")
    print(update_status(manager, "Finish Report", "In-Progress"))
    
    print("\n--- Search by Title 'Team' ---")
    results = search_by_title(manager, "Team")
    for t in results:
        print(vars(t))

if __name__ == "__main__":
    main()