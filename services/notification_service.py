import sqlite3
from data.database import DB_PATH
from datetime import datetime, timedelta

class NotificationService:
    @staticmethod
    def process_reminders():
        """Process due reminders and overdue tasks (TDRS-001-C)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=1)  # Process last minute
        
        # Find tasks with reminders in the processing window
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE reminder_time BETWEEN ? AND ?
            AND status != 'Completed'
        ''', (window_start.isoformat(), now.isoformat()))
        
        reminder_tasks = []
        for row in cursor.fetchall():
            task = dict(zip(['id', 'title', 'description', 'priority', 'status', 'due_date', 'reminder_time', 'created_at'], row))
            reminder_tasks.append(task)
            NotificationService._send_reminder(task)
        
        # Mark reminders as sent (add reminder_sent column in future iterations)
        
        conn.close()
        return reminder_tasks

    @staticmethod
    def _send_reminder(task):
        """Send reminder notification (mock implementation)"""
        print(f"🚨 REMINDER: Task '{task['title']}' due at {task.get('reminder_time')}")

    @staticmethod
    def process_overdue():
        """Process newly overdue tasks"""
        overdue_tasks = TaskService.get_overdue_tasks()
        for task in overdue_tasks:
            print(f"⏰ OVERDUE: Task '{task['title']}' was due on {task['due_date']}")