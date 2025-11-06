from tasks.cli_handler import run_cli
from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority

def main():
    manager = TaskManager()
    run_cli(manager)
    print("=== Welcome to Task Manager ===")

    # Sample flow for iteration 1
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

if __name__ == "__main__":
    main()
