from users.user_manager import UserManager
from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title

def show_main_menu(user):
    print(f"\n=== Task Manager ===")
    print(f"Logged in as: {user.username} ({user.role})")
    print("\n-- Main Menu --")
    print("1. List Tasks")
    print("2. Add Task")
    print("3. Update Task Status")
    print("4. Delete Task")
    print("5. Search Task by Title")
    print("6. Switch User")
    if user.role == "Admin":
        print("7. Manage Users")
    print("0. Logout and Exit")

def handle_admin_user_management(um, current_username):
    while True:
        print("\n-- Admin User Management --")
        print("1. Add User")
        print("2. Remove User")
        print("3. List Users")
        print("0. Back")
        choice = input("Select: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role (Admin/User): ").strip()
            print(um.add_user(username, password, role))
        elif choice == "2":
            username = input("Username to remove: ").strip()
            print(um.remove_user(username, current_username))
        elif choice == "3":
            for u in um.list_users():
                print(u)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")

def main():
    um = UserManager()
    user = None

    # Login phase
    while not user:
        print("=== Login ===")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        authenticated = um.authenticate(username, password)
        if authenticated:
            user = authenticated
        else:
            print("Invalid username or password. Please try again.")

    tm = TaskManager(current_user=user)

    # Main loop
    while True:
        show_main_menu(user)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n--- Task List ---")
            tasks = tm.list_tasks()
            if tasks:
                for t in tasks:
                    print(t)
            else:
                print("No tasks found.")
        elif choice == "2":
            title = input("Title: ").strip()
            desc = input("Description: ").strip()
            priority = input("Priority (Low/Medium/High): ").strip() or "Medium"
            tm.add_task(Task(title, desc, priority))
            print("Task added successfully.")
        elif choice == "3":
            title = input("Enter task title to update: ").strip()
            new_status = input("New Status (Pending/In-Progress/Completed): ").strip()
            print(update_status(tm, title, new_status))
        elif choice == "4":
            task_id = input("Enter task ID to delete: ").strip()
            print(tm.delete_task(task_id))
        elif choice == "5":
            query = input("Enter search keyword: ").strip()
            results = search_by_title(tm, query)
            print("\n--- Search Results ---")
            for t in results:
                print(vars(t))
        elif choice == "6":
            um.logout()
            main()  # restart login
            return
        elif choice == "7" and user.role == "Admin":
            handle_admin_user_management(um, user.username)
        elif choice == "0":
            um.logout()
            print("Logged out. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()