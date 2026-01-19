# Sample flow for iteration 1
from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority
from tasks.notifications import integrate_notifications_with_tasks

print("testing")
def main():
    manager = TaskManager()
    print("=== Welcome to Task Manager ===")

    
    # Add sample tasks
    manager.add_task(Task("Finish Report", "Complete the financial report", "High"))
    manager.add_task(Task("Email Client", "Send project updates", "Medium"))
    manager.add_task(Task("Team Meeting", "Discuss project roadmap", "Low"))

    # List all tasks
    print("\n--- All Tasks ---")
    for t in manager.list_tasks():
        print(t)

    # Update status
    print("\n--- Update Status ---")
    print(update_status(manager, "Finish Report", "In-Progress"))

    # Search tasks
    print("\n--- Search by Title 'Team' ---")
    results = search_by_title(manager, "Team")
    for t in results:
        print(vars(t))

    # NEW: Add notification integration
    print("\n--- Setting up Notifications ---")
    notifier = integrate_notifications_with_tasks(manager)
    
    print("\n--- Notification Stats ---")
    print(notifier.get_notification_stats())

if __name__ == "__main__":
    main()
