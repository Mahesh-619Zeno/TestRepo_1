from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority
from tasks.priority_category import validate_priority, validate_category
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
        print("\nCommands: add, list, update, search, exit")
        command = input("Enter command: ").strip().lower()
        if command == "add":
            title = input("Enter task title: ").strip()
            description = input("Enter task description: ").strip()
            try:
                priority_input = input("Enter priority (Low, Medium, High): ").strip()
                priority = validate_priority(priority_input)
                category_input = input("Enter category (e.g., Work, Personal, Study): ").strip()
                category = validate_category(category_input)
                task = Task(title, description, priority, category)
                manager.add_task(task)
                print(f"Task '{title}' added successfully with priority '{priority}' and category '{category}'.")
            except ValueError as e:
                print(e)
        elif command == "list":
            filter_priority = input_with_validation("Filter by priority (Low, Medium, High) or hit Enter to skip: ",
                                                    ["Low", "Medium", "High"], allow_empty=True)
            filter_category = input("Filter by category or hit Enter to skip: ").strip()
            sort_priority_input = input_with_validation("Sort by priority? (yes/no): ", ["yes", "no"])
            sort_priority = sort_priority_input.lower() == "yes"
            tasks = manager.list_tasks(filter_priority, filter_category if filter_category else None, sort_priority)
            if not tasks:
                print("No tasks found with the specified filters.")
            else:
                for t in tasks:
                    print(t)
        elif command == "update":
            title = input("Enter the title of task to update status: ").strip()
            new_status = input("Enter new status (Pending, In-Progress, Completed): ").strip()
            result = update_status(manager, title, new_status)
            print(result)
        elif command == "search":
            search_type = input_with_validation("Search by (title/priority): ", ["title", "priority"])
            if search_type == "title":
                query = input("Enter title search query: ")
                results = search_by_title(manager, query)
            else:
                priority_input = input_with_validation("Enter priority (Low, Medium, High): ", ["Low", "Medium", "High"])
                results = search_by_priority(manager, priority_input)
            if results:
                for t in results:
                    print(vars(t))
            else:
                print("No matching tasks found.")
        elif command == "exit":
            print("Exiting Task Manager.")
            break
        else:
            print("Unknown command. Try again.")
if __name__ == "__main__":
    main()