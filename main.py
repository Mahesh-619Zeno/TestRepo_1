import requests
import json

API_BASE = "http://localhost:5000"

def main():
    print("=== Task Manager with Deadlines & Reminders (TDRS-001) ===")
    
    # Test 1: Create tasks with deadlines (TDRS-001-A)
    print("\n--- 1. Creating Tasks with Deadlines ---")
    tasks_to_create = [
        {
            "title": "Finish Report",
            "description": "Complete financial report",
            "priority": "High",
            "dueDate": "2026-02-01T18:00:00Z",
            "reminderTime": "2026-01-30T10:00:00Z"
        },
        {
            "title": "Email Client", 
            "priority": "Medium",
            "dueDate": "2026-01-31T12:00:00Z"
        }
    ]
    
    for task_data in tasks_to_create:
        response = requests.post(f"{API_BASE}/tasks", json=task_data)
        print(f"Created: {response.json()}")
    
    # Test 2: List all tasks sorted by due date
    print("\n--- 2. All Tasks (Sorted by Due Date) ---")
    response = requests.get(f"{API_BASE}/tasks?sortBy=dueDate&order=asc")
    for task in response.json():
        print(f"ID:{task['id']} {task['title']} (Due: {task.get('due_date', 'No deadline')})")
    
    # Test 3: Check overdue tasks
    print("\n--- 3. Overdue Tasks ---")
    response = requests.get(f"{API_BASE}/tasks/overdue")
    overdue = response.json()
    if overdue:
        for task in overdue:
            print(f"OVERDUE: {task['title']} (Due: {task['due_date']})")
    else:
        print("No overdue tasks 🎉")

if __name__ == "__main__":
    print("Start API server first: python app.py")
    print("Then run: python main.py")
    main()
