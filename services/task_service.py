import sqlite3
from data.database import DB_PATH, validate_iso_datetime

class TaskService:
    @staticmethod
    def create_task(task_data):
        """Create a new task with deadline validation"""
        title = task_data.get('title')
        if not title:
            raise ValueError("Title is required")
        
        due_date = task_data.get('dueDate')
        reminder_time = task_data.get('reminderTime')
        
        if due_date:
            validate_iso_datetime(due_date)
        if reminder_time:
            validate_iso_datetime(reminder_time)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tasks (title, description, priority, status, due_date, reminder_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            title,
            task_data.get('description', ''),
            task_data.get('priority', 'Medium'),
            task_data.get('status', 'Pending'),
            due_date,
            reminder_time
        ))
        
        task_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return TaskService.get_task(task_id)

    @staticmethod
    def get_tasks(sort_by=None, order='asc'):
        """Get all tasks with optional sorting"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM tasks'
        params = []
        
        if sort_by == 'dueDate':
            query += ' ORDER BY due_date ' + ('ASC' if order.lower() == 'asc' else 'DESC')
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        tasks = []
        for row in rows:
            task = dict(zip(['id', 'title', 'description', 'priority', 'status', 'due_date', 'reminder_time', 'created_at'], row))
            tasks.append(task)
        
        conn.close()
        return tasks

    @staticmethod
    def get_overdue_tasks():
        """Get tasks that are overdue and not completed"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE due_date < datetime('now') 
            AND status != 'Completed'
        ''')
        
        rows = cursor.fetchall()
        tasks = []
        for row in rows:
            task = dict(zip(['id', 'title', 'description', 'priority', 'status', 'due_date', 'reminder_time', 'created_at'], row))
            tasks.append(task)
        
        conn.close()
        return tasks

    @staticmethod
    def get_task(task_id):
        """Get single task by ID"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(zip(['id', 'title', 'description', 'priority', 'status', 'due_date', 'reminder_time', 'created_at'], row))
        return None
