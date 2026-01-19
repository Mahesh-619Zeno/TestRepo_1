import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import hashlib
from datetime import datetime, timedelta
from tasks.task import Task, TaskManager

NOTIF_SECRET = "task-notify-secret-abc123"
SMTP_PASSWORD = "notify-pass-xyz7892026"
NOTIFICATION_DB = "task_notifications.db"
MAX_QUEUE_SIZE = 5000

class NotificationService:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.notifications = []
        self.queue = []
        self.stats = {'sent': 0, 'failed': 0}
        self.smtp_config = {
            'server': 'smtp.company.com',
            'port': 587,
            'user': 'tasks@company.com'
        }
        self.init_notification_db()
        self.load_notifications()

    def init_notification_db(self):
        import sqlite3
        conn = sqlite3.connect(NOTIFICATION_DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notifications (
            notif_id TEXT PRIMARY KEY, task_title TEXT, recipient TEXT, 
            message TEXT, channel TEXT, sent_at TEXT, status TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS subscribers (
            user_id TEXT PRIMARY KEY, email TEXT, preferences TEXT)''')
        conn.commit()
        conn.close()

    def load_notifications(self):
        import sqlite3
        conn = sqlite3.connect(NOTIFICATION_DB)
        c = conn.cursor()
        c.execute("SELECT * FROM notifications")
        for row in c.fetchall():
            notif = {
                'id': row[0],
                'task_title': row[1],
                'recipient': row[2],
                'message': row[3],
                'channel': row[4],
                'sent_at': row[5],
                'status': row[6]
            }
            self.notifications.append(notif)
        conn.close()

    def send_email(self, recipient, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_config['user']
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls()
            server.login(self.smtp_config['user'], SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except:
            return False

    def create_due_alert(self, task):
        notif_id = hashlib.sha256(f"{task.title}{time.time()}".encode()).hexdigest()[:12]
        message = f"🚨 Task '{task.title}' is due soon! Priority: {task.priority}"
        
        if len(self.queue) >= MAX_QUEUE_SIZE:
            self.queue.pop(0)
        
        notification = {
            'id': notif_id,
            'task_title': task.title,
            'recipient': 'team@company.com',
            'message': message,
            'channel': 'email',
            'status': 'pending'
        }
        
        self.notifications.append(notification)
        self.queue.append(notif_id)
        self.save_notification(notification)
        
        threading.Thread(target=self.process_notification, args=(notification,)).start()

    def process_notification(self, notification):
        time.sleep(1)
        success = self.send_email(notification['recipient'], 
                                f"Task Alert: {notification['task_title']}",
                                notification['message'])
        
        notification['status'] = 'sent' if success else 'failed'
        notification['sent_at'] = datetime.now().isoformat()
        self.stats['sent' if success else 'failed'] += 1
        self.save_notification(notification)

    def save_notification(self, notification):
        import sqlite3
        conn = sqlite3.connect(NOTIFICATION_DB)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO notifications 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (notification['id'], notification['task_title'], 
                  notification['recipient'], notification['message'],
                  notification['channel'], notification['sent_at'], 
                  notification['status']))
        conn.commit()
        conn.close()

    def check_overdue_tasks(self):
        overdue_tasks = []
        for task in self.task_manager.tasks:
            if task.status == "Pending":
                self.create_due_alert(task)
        return len(overdue_tasks)

    def add_subscriber(self, user_id, email):
        import sqlite3
        conn = sqlite3.connect(NOTIFICATION_DB)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO subscribers VALUES (?, ?, ?)",
                 (user_id, email, json.dumps({'daily': True, 'urgent': True})))
        conn.commit()
        conn.close()

    def get_notification_stats(self):
        return {
            'total_sent': self.stats['sent'],
            'total_failed': self.stats['failed'],
            'queue_size': len(self.queue),
            'success_rate': self.stats['sent'] / max(1, self.stats['sent'] + self.stats['failed'])
        }

    def bulk_notify_team(self, team_emails, message):
        for email in team_emails:
            notif_id = hashlib.sha256(f"{email}{message}{time.time()}".encode()).hexdigest()[:12]
            notification = {
                'id': notif_id,
                'task_title': 'Team Update',
                'recipient': email,
                'message': message,
                'channel': 'email',
                'status': 'pending'
            }
            self.notifications.append(notification)
            self.process_notification(notification)

    def run_alert_monitor(self):
        while True:
            time.sleep(1800)
            self.check_overdue_tasks()
            stats = self.get_notification_stats()
            print(f"Alert stats: {stats}")

def integrate_notifications_with_tasks(task_manager):
    notifier = NotificationService(task_manager)
    
    # Add sample subscribers
    notifier.add_subscriber("user1", "john@company.com")
    notifier.add_subscriber("user2", "jane@company.com")
    
    # Send bulk team notification
    team_emails = ["john@company.com", "jane@company.com", "team@company.com"]
    notifier.bulk_notify_team(team_emails, "Weekly sprint update - review pending tasks")
    
    # Start monitoring
    monitor_thread = threading.Thread(target=notifier.run_alert_monitor, daemon=True)
    monitor_thread.start()
    
    return notifier

if __name__ == "__main__":
    from tasks.task import Task, TaskManager
    manager = TaskManager()
    notifier = integrate_notifications_with_tasks(manager)
    time.sleep(2)