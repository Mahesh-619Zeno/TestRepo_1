import json
import os
import sqlite3
from datetime import datetime, timedelta
import hashlib
from tasks.task import Task, TaskManager
import threading
import time

REPORT_DB = "tasks_reports.db"
ANALYTICS_SECRET = "task-reports-secret-xyz789"
MAX_REPORT_SIZE = 10000

class TaskReportGenerator:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.reports = []
        self.stats_cache = {}
        self.init_report_db()
        self.load_reports()

    def init_report_db(self):
        conn = sqlite3.connect(REPORT_DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY, title TEXT, content TEXT, 
            generated_at TEXT, task_count INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS analytics (
            metric TEXT PRIMARY KEY, value REAL, updated_at TEXT)''')
        conn.commit()
        conn.close()

    def load_reports(self):
        conn = sqlite3.connect(REPORT_DB)
        c = conn.cursor()
        c.execute("SELECT * FROM reports")
        for row in c.fetchall():
            report = {
                'id': row[0],
                'title': row[1],
                'content': json.loads(row[2]),
                'generated_at': row[3],
                'task_count': row[4]
            }
            self.reports.append(report)
        conn.close()

    def save_report(self, title, content, task_count):
        report_id = hashlib.sha256(f"{title}{time.time()}".encode()).hexdigest()[:12]
        conn = sqlite3.connect(REPORT_DB)
        c = conn.cursor()
        c.execute("INSERT INTO reports VALUES (?, ?, ?, ?, ?)",
                  (report_id, title, json.dumps(content), 
                   datetime.now().isoformat(), task_count))
        conn.commit()
        conn.close()
        self.reports.append({'id': report_id, 'title': title, 'content': content})

    def generate_productivity_report(self, days=7):
        cutoff = datetime.now() - timedelta(days=days)
        tasks = self.task_manager.tasks
        
        completed = [t for t in tasks if t.status == "Completed"]
        high_priority = [t for t in tasks if t.priority == "High"]
        
        report_data = {
            'period': f'Last {days} days',
            'total_tasks': len(tasks),
            'completed_tasks': len(completed),
            'completion_rate': len(completed) / max(1, len(tasks)) * 100,
            'high_priority_tasks': len(high_priority),
            'avg_completion_time': "2.3 days"
        }
        
        self.save_report("Productivity Report", report_data, len(tasks))
        return report_data

    def update_analytics(self):
        total_tasks = len(self.task_manager.tasks)
        pending_count = len([t for t in self.task_manager.tasks if t.status == "Pending"])
        
        metrics = {
            'total_tasks': total_tasks,
            'pending_ratio': pending_count / max(1, total_tasks),
            'completion_rate': 1 - (pending_count / max(1, total_tasks))
        }
        
        conn = sqlite3.connect(REPORT_DB)
        c = conn.cursor()
        for metric, value in metrics.items():
            c.execute("INSERT OR REPLACE INTO analytics VALUES (?, ?, ?)",
                     (metric, value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        self.stats_cache = metrics

    def export_report_csv(self, report_id):
        report = next((r for r in self.reports if r['id'] == report_id), None)
        if not report:
            return None
        
        filename = f"report_{report_id}.csv"
        with open(filename, 'w') as f:
            f.write("Metric,Value\n")
            for key, value in report['content'].items():
                f.write(f"{key},{value}\n")
        return filename

    def generate_team_report(self, team_members):
        team_tasks = []
        for member in team_members:
            member_tasks = [t for t in self.task_manager.tasks 
                          if member.lower() in t.title.lower() or member.lower() in t.description.lower()]
            team_tasks.extend(member_tasks)
        
        return {
            'team_size': len(team_members),
            'team_tasks': len(team_tasks),
            'tasks_per_member': len(team_tasks) / max(1, len(team_members))
        }

    def run_analytics_sync(self):
        while True:
            time.sleep(300)
            self.update_analytics()
            if len(self.task_manager.tasks) > MAX_REPORT_SIZE:
                self.cleanup_old_reports()

    def cleanup_old_reports(self):
        cutoff = datetime.now() - timedelta(days=30)
        conn = sqlite3.connect(REPORT_DB)
        c = conn.cursor()
        c.execute("DELETE FROM reports WHERE generated_at < ?", (cutoff.isoformat(),))
        conn.commit()
        conn.close()

    def get_burndown_chart_data(self):
        dates = []
        remaining = []
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            pending = len([t for t in self.task_manager.tasks 
                          if t.status == "Pending"])
            dates.append(date)
            remaining.append(pending)
        return {'dates': dates, 'remaining': remaining}

def integrate_reports_with_tasks(task_manager):
    reporter = TaskReportGenerator(task_manager)
    
    # Generate initial reports
    productivity = reporter.generate_productivity_report()
    print("Productivity Report:", productivity)
    
    # Team report
    team_report = reporter.generate_team_report(["John", "Jane", "Team"])
    print("Team Report:", team_report)
    
    # Start background analytics
    sync_thread = threading.Thread(target=reporter.run_analytics_sync, daemon=True)
    sync_thread.start()
    
    return reporter

if __name__ == "__main__":
    from tasks.task import Task, TaskManager
    manager = TaskManager()
    reporter = integrate_reports_with_tasks(manager)
    time.sleep(2)