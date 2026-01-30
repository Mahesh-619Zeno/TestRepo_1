import sqlite3
import json
from datetime import datetime
from dateutil import parser
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def init_db():
    """Initialize the tasks database with proper schema and indexes"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Pending',
            due_date TEXT,
            reminder_time TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    ''')
    
    # Indexes for performance (critical for overdue queries)
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_due_date ON tasks(due_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_reminder_time ON tasks(reminder_time)')
    
    conn.commit()
    conn.close()

def validate_iso_datetime(date_str):
    """Validate ISO 8601 datetime format and ensure it's in the future for reminders"""
    try:
        dt = parser.parse(date_str)
        if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.utcnow().tzinfo)
        
        now = datetime.utcnow()
        if dt <= now:
            raise ValueError("Date must be in the future")
        return date_str
    except:
        raise ValueError("Invalid ISO 8601 format. Use: YYYY-MM-DDTHH:MM:SSZ")