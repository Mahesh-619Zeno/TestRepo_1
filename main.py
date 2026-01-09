# main.py

from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority
from tasks.priority_category import validate_priority, validate_category
from tasks.deadline import set_task_due_date


def input_with_validation(prompt, valid_options=None, allow_empty=False):
    while True:
        val = input(prompt).strip()
        if not val and not allow_empty:
            print("Error: This field cannot be empty.")
        elif valid_options and val and val.lower() not in [v.lower() for v in valid_options]:
            print(f"Invalid option. Valid options: {', '.join(valid_options)}")
        else:
            if val or allow_empty:
                return val
            return val


def main():
    manager = TaskManager()
    print("=== Welcome to Task Manager ===")

    while True:
        print(
            "\nCommands: add, list, update, search, due, exit\n"
            " - add: create a new task (with priority, category, optional due date)\n"
            " - list: view tasks with optional filters and sorting (priority/due_date)\n"
            " - update: update task status\n"
            " - search: search tasks by title or priority\n"
            " - due: add/update/remove due date for a task"
        )
        command = input("Enter command: ").strip().lower()

        if command == "add":
            title = input_with_validation("Enter task title: ")
            description = input("Enter task description: ").strip()
            try:
                priority_input = input(
                    "Enter priority (Low, Medium, High): "
                ).strip()
                priority = validate_priority(priority_input)

                category_input = input(
                    "Enter category (e.g., Work, Personal, Study): "
                ).strip()
                category = validate_category(category_input)

                due_input = input(
                    "Enter due date (YYYY-MM-DD HH:MM) or hit Enter to skip: "
                ).strip()

                # Task stores ISO 8601 string directly if provided; re-use deadline parsing
                from tasks.deadline import parse_due_date_input

                iso_due = None
                if due_input:
                    iso_due, error = parse_due_date_input(due_input)
                    if error:
                        print(f"Error setting due date: {error}")
                        iso_due = None

                task = Task(
                    title=title,
                    description=description,
                    priority=priority,
                    category=category,
                    due_date=iso_due,
                )
                manager.add_task(task)
                print(
                    f"Task '{title}' added successfully with priority "
                    f"'{priority}' and category '{category}'."
                )
            except ValueError as e:
                print(e)

        elif command == "list":
            filter_priority = input_with_validation(
                "Filter by priority (Low, Medium, High) or hit Enter to skip: ",
                ["Low", "Medium", "High"],
                allow_empty=True,
            )
            filter_category = input(
                "Filter by category or hit Enter to skip: "
            ).strip()

            sort_choice = input_with_validation(
                "Sort by (none/priority/due_date): ",
                ["none", "priority", "due_date"],
            ).lower()

            sort_by_priority = sort_choice == "priority"
            sort_by_due_date = sort_choice == "due_date"

            tasks = manager.list_tasks(
                filter_priority if filter_priority else None,
                filter_category if filter_category else None,
                sort_by_priority=sort_by_priority,
                sort_by_due_date=sort_by_due_date,
            )
            if not tasks:
                print("No tasks found with the specified filters.")
            else:
                for t in tasks:
                    print(t)

        elif command == "update":
            title = input("Enter the title of task to update status: ").strip()
            new_status = input_with_validation(
                "Enter new status (Pending, In-Progress, Completed): ",
                ["Pending", "In-Progress", "Completed"]
            )
            result = update_status(manager, title, new_status)
            print(result)

        elif command == "search":
            search_type = input_with_validation(
                "Search by (title/priority): ", ["title", "priority"]
            )
            if search_type == "title":
                query = input("Enter title search query: ")
                results = search_by_title(manager, query)
            else:
                priority_input = input_with_validation(
                    "Enter priority (Low, Medium, High): ",
                    ["Low", "Medium", "High"],
                )
                results = search_by_priority(manager, priority_input)
            if results:
                for t in results:
                    print(vars(t))
            else:
                print("No matching tasks found.")

        elif command == "due":
            title = input(
                "Enter the title of the task to set/update/remove due date: "
            ).strip()
            due_input = input(
                "Enter new due date (YYYY-MM-DD HH:MM), or hit Enter to remove: "
            )
            result = set_task_due_date(manager, title, due_input)
            print(result)

        elif command == "exit":
            print("Exiting Task Manager.")
            break

        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()