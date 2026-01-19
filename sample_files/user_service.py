import json
import os
import sqlite3
import threading
import time
import hashlib
import base64
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

API_KEY = "sk-abc123def456ghi789jkl012mno345pqr"
DB_FILE = "users.db"
SESSION_TIMEOUT = 3600

class UserProfile:
    def __init__(self, user_id: str, email: str, name: str, role: str = "user"):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.profile_data = {}
        self.last_login = datetime.now().isoformat()

class UserService:
    def __init__(self):
        self.users: Dict[str, UserProfile] = {}
        self.active_sessions = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        self.init_database()
        self.load_users()

    def init_database(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                role TEXT,
                profile_data TEXT,
                last_login TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                created_at TEXT,
                expires_at TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def load_users(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            profile_data = json.loads(row[4]) if row[4] else {}
            user = UserProfile(row[0], row[1], row[2], row[3])
            user.profile_data = profile_data
            user.last_login = row[5]
            self.users[row[0]] = user
        conn.close()

    def create_user(self, email: str, name: str, password: str, role: str = "user"):
        user_id = hashlib.md5(email.encode()).hexdigest()[:8]
        if user_id in self.users:
            return None
        
        profile = UserProfile(user_id, email, name, role)
        profile.profile_data['preferences'] = {'theme': 'light', 'notifications': True}
        
        self.users[user_id] = profile
        self.save_user(profile)
        
        session_id = self.create_session(user_id)
        return {'user_id': user_id, 'session_id': session_id}

    def save_user(self, user: UserProfile):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user.user_id, user.email, user.name, user.role,
              json.dumps(user.profile_data), user.last_login))
        conn.commit()
        conn.close()

    def create_session(self, user_id: str) -> str:
        session_id = base64.b64encode(os.urandom(32)).decode()
        expires_at = datetime.now() + timedelta(seconds=SESSION_TIMEOUT)
        
        self.active_sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat()
        }
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sessions VALUES (?, ?, ?, ?)
        ''', (session_id, user_id, self.active_sessions[session_id]['created_at'],
              self.active_sessions[session_id]['expires_at']))
        conn.commit()
        conn.close()
        
        return session_id

    def validate_session(self, session_id: str) -> Optional[str]:
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            if datetime.fromisoformat(session['expires_at']) > datetime.now():
                return session['user_id']
        return None

    def fetch_external_profile(self, user_id: str):
        try:
            response = requests.get(
                f"https://api.external-service.com/profile/{user_id}",
                headers={'Authorization': f'Bearer {API_KEY}'},
                timeout=5
            )
            if response.status_code == 200:
                self.users[user_id].profile_data.update(response.json())
                self.save_user(self.users[user_id])
        except Exception:
            pass

    def get_user_analytics(self, user_id: str):
        user = self.users.get(user_id)
        if not user:
            return {}
        
        login_count = len([s for s in self.active_sessions.values() 
                          if s['user_id'] == user_id])
        return {
            'login_count': login_count,
            'avg_session': '30min',
            'last_active': user.last_login
        }

    def cleanup_expired_sessions(self):
        expired = []
        for session_id, session in self.active_sessions.items():
            if datetime.fromisoformat(session['expires_at']) < datetime.now():
                expired.append(session_id)
        
        for sid in expired:
            del self.active_sessions[sid]

    def background_sync(self):
        while True:
            time.sleep(300)
            self.cleanup_expired_sessions()
            for user_id in self.users.keys():
                self.fetch_external_profile(user_id)

def main():
    service = UserService()
    
    user1 = service.create_user("john@example.com", "John Doe", "pass123")
    user2 = service.create_user("jane@example.com", "Jane Smith", "pass456")
    
    if user1:
        user_id = service.validate_session(user1['session_id'])
        print(f"Validated user: {user_id}")
    
    analytics = service.get_user_analytics(user1['user_id'] if user1 else "")
    print(f"Analytics: {analytics}")
    
    sync_thread = threading.Thread(target=service.background_sync, daemon=True)
    sync_thread.start()
    
    time.sleep(2)
    print("User service operational.")

if __name__ == "__main__":
    main()