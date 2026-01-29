from tasks.task import Task, TaskManager
from tasks.status import update_status
from tasks.search import search_by_title, search_by_priority
from tasks.deadline import validate_due_date, validate_reminder_time
from datetime import datetime, timedelta
import pytz

def main():
    manager = TaskManager()
    print("=== Welcome to Task Manager with Deadlines ===")

    # Add sample tasks with deadlines and reminders
    now = datetime.now(pytz.UTC)
    task1 = Task("Finish Report", "Complete the financial report", "High", 
                 due_date=(now + timedelta(hours=2)).isoformat(), reminder_time=60)
    task2 = Task("Email Client", "Send project updates", "Medium",
                 due_date=(now + timedelta(days=1)).isoformat(), reminder_time=120)
    task3 = Task("Team Meeting", "Discuss project roadmap", "Low")

    for t in [task1, task2, task3]:
        manager.add_task(t)

    print("\n--- All Tasks Sorted by Due Date ASC ---")
    for t in manager.list_tasks(sort_by_due_date="asc"):
        due = t["Due Date"] if t["Due Date"] else "No due date"
        print(f"{t['Title']} - Status: {t['Status']} - Due: {due}")

if __name__ == "__main__":
    main()