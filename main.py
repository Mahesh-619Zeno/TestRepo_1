from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority

def input_with_validation(prompt, valid_options=None, allow_empty=False):
    while True:
        val = input(prompt).strip()
        if not val and allow_empty:
            return val
        if valid_options and val.lower() not in [v.lower() for v in valid_options]:
            print(f"Invalid option. Valid options: {', '.join(valid_options)}")
        else:
            return val

def main():
    manager = TaskManager()
    print("=== Welcome to Task Manager ===")

    while True:
        print(
            "\nCommands: add, list, update, search, exit\n"
            " - add: create a new task (priority, category)\n"
            " - list: view tasks\n"
            " - update: update task status\n"
            " - search: search tasks by title or priority\n"
            " - exit: quit the program"
        )
        command = input("Enter command: ").strip().lower()

        if command == "add":
            title = input("Enter task title: ").strip()
            description = input("Enter task description: ").strip()
            try:
                priority = input_with_validation(
                    "Enter priority (Low, Medium, High): ",
                    ["Low", "Medium", "High"]
                )
                category = input("Enter category (Work, Personal, Study): ").strip()

                task = Task(title=title, description=description, priority=priority, category=category)
                manager.add_task(task)
                print(f"Task '{title}' added successfully.")
            except ValueError as e:
                print(e)

        elif command == "list":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks available.")
            else:
                for t in tasks:
                    print(t)

        elif command == "update":
            title = input("Enter the title of task to update status: ").strip()
            new_status = input_with_validation(
                "Enter new status (Pending, In-Progress, Completed): ",
                ["Pending", "In-Progress", "Completed"]
            )
            print(update_status(manager, title, new_status))

        elif command == "search":
            search_type = input_with_validation(
                "Search by (title/priority): ",
                ["title", "priority"]
            )
            if search_type == "title":
                query = input("Enter title search query: ")
                results = search_by_title(manager, query)
            else:
                priority_input = input_with_validation(
                    "Enter priority (Low, Medium, High): ",
                    ["Low", "Medium", "High"]
                )
                results = search_by_priority(manager, priority_input)

            if results:
                for t in results:
                    print(t)
            else:
                print("No matching tasks found.")

        elif command == "exit":
            print("Exiting Task Manager.")
            break

        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    main()
