import argparse
from tasks.task import Task, TaskManager
from tasks.search import search_by_title, search_by_priority, search_by_category
from tasks.status import update_status

def run_cli(manager=None):
    parser = argparse.ArgumentParser(description="Task Manager CLI with prioritization and categorization.")
    subparsers = parser.add_subparsers(dest="command")
    parser.required = True

    # Create Command: priority and category optional with defaults
    create_parser = subparsers.add_parser("create", help="Create a new task.")
    create_parser.add_argument("--title", required=True, help="Task title.")
    create_parser.add_argument("--description", default="", help="Task description.")
    create_parser.add_argument("--priority", default="Medium", choices=["Low", "Medium", "High"], help="Task priority (default: Medium).")
    create_parser.add_argument("--category", default="General", help="Task category (default: General).")

    # List Command: optional filters, no required arguments
    list_parser = subparsers.add_parser("list", help="List tasks.")
    list_parser.add_argument("--filter-priority", choices=["Low", "Medium", "High"], help="Filter by priority.")
    list_parser.add_argument("--filter-category", help="Filter by category.")
    list_parser.add_argument("--sort", choices=["priority"], help="Sort tasks by priority.")

    # Update Command
    update_parser = subparsers.add_parser("update-status", help="Update task status.")
    update_parser.add_argument("--title", required=True, help="Task title.")
    update_parser.add_argument("--new-status", required=True, help="New status.")

    # Search Command with optional arguments
    search_parser = subparsers.add_parser("search", help="Search tasks.")
    search_parser.add_argument("--title", help="Search by title substring.")
    search_parser.add_argument("--priority", choices=["Low", "Medium", "High"], help="Search by priority.")
    search_parser.add_argument("--category", help="Search by category.")

    args = parser.parse_args()

    if manager is None:
        manager = TaskManager()

    try:
        if args.command == "create":
            task = Task(args.title, args.description, args.priority, args.category)
            manager.add_task(task)
            print(f"Task '{args.title}' created successfully with priority '{args.priority}' and category '{args.category}'.")

        elif args.command == "list":
            tasks = manager.list_tasks(args.filter_priority, args.filter_category, args.sort == "priority")
            if isinstance(tasks, str):
                print(tasks)
            else:
                for t in tasks:
                    print(t)

        elif args.command == "update-status":
            print(update_status(manager, args.title, args.new_status))

        elif args.command == "search":
            results = []
            if args.title:
                results = search_by_title(manager, args.title)
            elif args.priority:
                results = search_by_priority(manager, args.priority)
            elif args.category:
                results = search_by_category(manager, args.category)

            if not results:
                print("No matching tasks found.")
            else:
                for t in results:
                    print(vars(t))
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Error: {e}")
