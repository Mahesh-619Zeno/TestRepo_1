import json
import os
from datetime import datetime, timedelta
import pytz  # For timezone handling

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/tasks_data.json")

class Task:
    def __init__(self, title, description="", priority="Medium", 
                 due_date=None, reminder_time=None, is_recurring=False, recurrence_pattern=None,
                 status="Pending"):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = self._parse_datetime(due_date)
        self.reminder_time = reminder_time  # in minutes before due_date
        self.is_recurring = is_recurring
        self.recurrence_pattern = recurrence_pattern

    def _parse_datetime(self, dt):
        if dt is None:
            return None
        if isinstance(dt, datetime):
            return dt
        # Expecting ISO format string:
        try:
            # Store datetime in UTC internally
            dt_obj = datetime.fromisoformat(dt)
            if dt_obj.tzinfo is None:
                # Assume UTC if no tzinfo
                dt_obj = dt_obj.replace(tzinfo=pytz.UTC)
            else:
                dt_obj = dt_obj.astimezone(pytz.UTC)
            return dt_obj
        except Exception:
            return None

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reminder_time": self.reminder_time,
            "is_recurring": self.is_recurring,
            "recurrence_pattern": self.recurrence_pattern
        }

    def update_due_date(self, due_date):
        new_due_date = self._parse_datetime(due_date)
        if new_due_date:
            self.due_date = new_due_date
        else:
            raise ValueError("Invalid due_date format")

    def update_reminder_time(self, reminder_time):
        # reminder_time in minutes (int or None)
        if reminder_time is None:
            self.reminder_time = None
        else:
            reminder_int = int(reminder_time)
            if self.due_date:
                reminder_dt = self.due_date - timedelta(minutes=reminder_int)
                if reminder_dt < datetime.now(pytz.UTC):
                    raise ValueError("Reminder time must be before due date and in future.")
            self.reminder_time = reminder_int

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def get_task(self, title):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        return None

    def update_task(self, task):
        for i, t in enumerate(self.tasks):
            if t.title.lower() == task.title.lower():
                self.tasks[i] = task
                self.save_tasks()
                return True
        return False

    def list_tasks(self, sort_by_due_date=None):
        task_list = [{
            "Title": t.title,
            "Description": t.description,
            "Priority": t.priority,
            "Status": t.status,
            "Due Date": t.due_date.isoformat() if t.due_date else None,
            "Is Recurring": t.is_recurring,
            "Recurrence Pattern": t.recurrence_pattern,
            "Reminder Time (minutes)": t.reminder_time
        } for t in self.tasks]
        if sort_by_due_date == "asc":
            task_list.sort(key=lambda x: x["Due Date"] or "")
        elif sort_by_due_date == "desc":
            task_list.sort(key=lambda x: x["Due Date"] or "", reverse=True)
        return task_list

    def save_tasks(self):
        data = [t.to_dict() for t in self.tasks]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load_tasks(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = [Task(**d) for d in data]