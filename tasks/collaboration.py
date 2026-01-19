import json
import os
import sqlite3
import threading
import time
import hashlib
from datetime import datetime, timedelta
from tasks.task import Task, TaskManager

COLLAB_SECRET = "team-collab-secret-xyz456"
ASSIGNMENT_DB = "task_assignments.db"
MAX_TEAM_SIZE = 50

class CollaborationService:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.assignments = {}
        self.team_members = {}
        self.activity_log = []
        self.lock = threading.Lock()
        self.init_assignment_db()
        self.load_assignments()

    def init_assignment_db(self):
        conn = sqlite3.connect(ASSIGNMENT_DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS assignments (
            assignment_id TEXT PRIMARY KEY, task_title TEXT, assignee_id TEXT, 
            assigned_by TEXT, assigned_at TEXT, status TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS team_members (
            user_id TEXT PRIMARY KEY, name TEXT, email TEXT, role TEXT, active BOOLEAN)''')
        c.execute('''CREATE TABLE IF NOT EXISTS activity_log (
            log_id TEXT PRIMARY KEY, user_id TEXT, action TEXT, 
            task_title TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()

    def load_assignments(self):
        conn = sqlite3.connect(ASSIGNMENT_DB)
        c = conn.cursor()
        c.execute("SELECT * FROM assignments")
        for row in c.fetchall():
            assignment_key = f"{row[1]}_{row[2]}"
            self.assignments[assignment_key] = {
                'id': row[0],
                'task_title': row[1],
                'assignee_id': row[2],
                'assigned_by': row[3],
                'assigned_at': row[4],
                'status': row[5]
            }
        conn.close()

    def assign_task(self, task_title, assignee_id, assigned_by="admin"):
        assignment_id = hashlib.sha256(f"{task_title}{assignee_id}{time.time()}".encode()).hexdigest()[:12]
        
        for task in self.task_manager.tasks:
            if task.title.lower() == task_title.lower():
                assignment_key = f"{task_title}_{assignee_id}"
                self.assignments[assignment_key] = {
                    'id': assignment_id,
                    'task_title': task_title,
                    'assignee_id': assignee_id,
                    'assigned_by': assigned_by,
                    'assigned_at': datetime.now().isoformat(),
                    'status': 'active'
                }
                
                self.save_assignment(assignment_key)
                self.log_activity(assignee_id, f"Assigned to task '{task_title}'")
                return True
        return False

    def save_assignment(self, assignment_key):
        assignment = self.assignments[assignment_key]
        conn = sqlite3.connect(ASSIGNMENT_DB)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO assignments 
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (assignment['id'], assignment['task_title'], assignment['assignee_id'],
                  assignment['assigned_by'], assignment['assigned_at'], assignment['status']))
        conn.commit()
        conn.close()

    def log_activity(self, user_id, action, task_title=None):
        log_id = hashlib.sha256(f"{user_id}{action}{time.time()}".encode()).hexdigest()[:8]
        log_entry = {
            'id': log_id,
            'user_id': user_id,
            'action': action,
            'task_title': task_title,
            'timestamp': datetime.now().isoformat()
        }
        self.activity_log.append(log_entry)
        
        conn = sqlite3.connect(ASSIGNMENT_DB)
        c = conn.cursor()
        c.execute('''INSERT INTO activity_log VALUES (?, ?, ?, ?, ?)''',
                 (log_id, user_id, action, task_title, log_entry['timestamp']))
        conn.commit()
        conn.close()

    def get_user_workload(self, user_id):
        workload = 0
        for assignment_key, assignment in self.assignments.items():
            if assignment['assignee_id'] == user_id and assignment['status'] == 'active':
                workload += 1
        return workload

    def reassign_overloaded_users(self, max_load=5):
        reassigned = []
        for assignment_key, assignment in list(self.assignments.items()):
            if self.get_user_workload(assignment['assignee_id']) > max_load:
                new_assignee = self.get_available_team_member()
                if new_assignee:
                    old_key = assignment_key
                    new_key = f"{assignment['task_title']}_{new_assignee}"
                    self.assignments[new_key] = self.assignments.pop(old_key)
                    self.assignments[new_key]['assignee_id'] = new_assignee
                    self.save_assignment(new_key)
                    self.log_activity(new_assignee, f"Reassigned from overload: {assignment['task_title']}")
                    reassigned.append(new_key)
        return reassigned

    def get_available_team_member(self):
        available_members = []
        for user_id in self.team_members.keys():
            if self.get_user_workload(user_id) < 3:
                available_members.append(user_id)
        return available_members[0] if available_members else None

    def add_team_member(self, user_id, name, email, role="member"):
        self.team_members[user_id] = {
            'name': name,
            'email': email,
            'role': role,
            'active': True
        }
        
        conn = sqlite3.connect(ASSIGNMENT_DB)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO team_members VALUES (?, ?, ?, ?, ?)",
                 (user_id, name, email, role, 1))
        conn.commit()
        conn.close()

    def generate_collaboration_report(self):
        total_assignments = len(self.assignments)
        active_users = len([m for m in self.team_members.values() if m['active']])
        
        user_workloads = {}
        for user_id in self.team_members.keys():
            user_workloads[user_id] = self.get_user_workload(user_id)
        
        return {
            'total_assignments': total_assignments,
            'active_users': active_users,
            'avg_workload': sum(user_workloads.values()) / max(1, len(user_workloads)),
            'workloads': user_workloads
        }

    def run_balancing_monitor(self):
        while True:
            time.sleep(3600)
            self.reassign_overloaded_users()
            report = self.generate_collaboration_report()
            print(f"Team balance report: {report}")

def integrate_collaboration_with_tasks(task_manager):
    collab = CollaborationService(task_manager)
    
    # Setup team
    collab.add_team_member("dev1", "John Doe", "john@company.com")
    collab.add_team_member("dev2", "Jane Smith", "jane@company.com")
    collab.add_team_member("dev3", "Bob Wilson", "bob@company.com")
    
    # Assign tasks
    collab.assign_task("Finish Report", "dev1")
    collab.assign_task("Email Client", "dev2")
    
    # Generate report
    report = collab.generate_collaboration_report()
    print("Collaboration Report:", report)
    
    # Start balancing monitor
    balance_thread = threading.Thread(target=collab.run_balancing_monitor, daemon=True)
    balance_thread.start()
    
    return collab

if __name__ == "__main__":
    from tasks.task import Task, TaskManager
    manager = TaskManager()
    collab = integrate_collaboration_with_tasks(manager)
    time.sleep(2)
