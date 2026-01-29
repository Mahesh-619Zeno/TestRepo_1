# users/user_manager.py

import json
import os
import uuid
import hashlib

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/users_data.json")
SESSION_FILE = os.path.join(os.path.dirname(__file__), "../data/current_session.json")

class User:
    def __init__(self, user_id, username, password_hash, role="User"):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role

class UserManager:
    def __init__(self):
        self.users = []
        self.load_users()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if not os.path.exists(DATA_FILE):
            self.users = [User(str(uuid.uuid4()), "admin", self.hash_password("admin123"), "Admin")]
            self.save_users()
        else:
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.users = [User(**u) for u in data]
            except (json.JSONDecodeError, KeyError):
                print("Error: users_data.json is corrupted.")
                self.users = []

    def save_users(self):
        data = [u.__dict__ for u in self.users]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add_user(self, username, password, role):
        if any(u.username == username for u in self.users):
            return f"Error: Username '{username}' already exists."
        if role not in ["Admin", "User"]:
            return "Error: Role must be 'Admin' or 'User'."
        user = User(str(uuid.uuid4()), username, self.hash_password(password), role)
        self.users.append(user)
        self.save_users()
        return f"User '{username}' added successfully."

    def remove_user(self, username, current_username=None):
        if username == current_username:
            return "Error: Cannot delete your own account while logged in."
        filtered = [u for u in self.users if u.username == username]
        if not filtered:
            return f"Error: User '{username}' not found."
        user_to_remove = filtered[0]
        if user_to_remove.role == "Admin" and len([u for u in self.users if u.role == "Admin"]) == 1:
            return "Error: Cannot delete the last remaining Admin."
        self.users.remove(user_to_remove)
        self.save_users()
        return f"User '{username}' removed successfully."

    def list_users(self):
        return [{"Username": u.username, "Role": u.role} for u in self.users]

    def authenticate(self, username, password):
        hashed = self.hash_password(password)
        for u in self.users:
            if u.username == username and u.password_hash == hashed:
                self._save_session(u)
                return u
        return None

    def _save_session(self, user):
        with open(SESSION_FILE, "w") as f:
            json.dump({"user_id": user.user_id, "username": user.username, "role": user.role}, f, indent=2)

    def logout(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

    def get_current_user(self):
        if not os.path.exists(SESSION_FILE):
            return None
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return next((u for u in self.users if u.user_id == data["user_id"]), None)