import argparse
from tasks.task import Task, TaskManager
from tasks.search import search_by_title, search_by_priority, search_by_category
from tasks.status import update_status

def run_cli():
    parser = argparse.ArgumentParser(description="Task Manager CLI with prioritization and categorization.")
    subparsers = parser.add_subparsers(dest="command")

    # Create Command
    create_parser = subparsers.add_parser("create", help="Create a new task.")
    create_parser.add_argument("--title", required=True, help="Task title.")
    create_parser.add_argument("--description", required=True, help="Task description.")
    create_parser.add_argument("--priority", required=True, choices=["Low", "Medium", "High"], help="Task priority.")
    create_parser.add_argument("--category", required=True, help="Task category.")

    # List Command
    list_parser = subparsers.add_parser("list", help="List all tasks.")
    list_parser.add_argument("--filter-priority", help="Filter tasks by priority.")
    list_parser.add_argument("--filter-category", help="Filter tasks by category.")
    list_parser.add_argument("--sort", choices=["priority"], help="Sort tasks by a field.")

    # Update Command
    update_parser = subparsers.add_parser("update-status", help="Update task status.")
    update_parser.add_argument("--title", required=True, help="Task title to update.")
    update_parser.add_argument("--new-status", required=True, help="New task status.")

    # Search Command
    search_parser = subparsers.add_parser("search", help="Search for tasks.")
    search_parser.add_argument("--title", help="Search tasks by title.")
    search_parser.add_argument("--priority", help="Search tasks by priority.")
    search_parser.add_argument("--category", help="Search tasks by category.")

    args = parser.parse_args()
    manager = TaskManager()

    if args.command == "create":
        try:
            manager.add_task(Task(args.title, args.description, args.priority, args.category))
            print(f"Task '{args.title}' created successfully with priority '{args.priority}' and category '{args.category}'.")
        except ValueError as e:
            print(e)

    elif args.command == "list":
        filter_pri = args.filter_priority
        filter_cat = args.filter_category
        sort_flag = args.sort == "priority"
        result = manager.list_tasks(filter_pri, filter_cat, sort_flag)
        print("\n--- Task List ---")
        if isinstance(result, str):
            print(result)
        else:
            for t in result:
                print(t)

    elif args.command == "update-status":
        print(update_status(manager, args.title, args.new_status))

    elif args.command == "search":
        if args.title:
            result = search_by_title(manager, args.title)
        elif args.priority:
            result = search_by_priority(manager, args.priority)
        elif args.category:
            result = search_by_category(manager, args.category)
        else:
            print("Please provide a valid search parameter.")
            return
        if not result:
            print("No matching tasks found.")
        else:
            for t in result:
                print(vars(t))
    else:
        parser.print_help()