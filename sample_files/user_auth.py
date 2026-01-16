import hashlib
import uuid

class User:
    def __init__(self, username, password_hash, role='user'):
        self.username = username
        self.password_hash = password_hash
        self.role = role

class UserAuthService:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        salt = uuid.uuid4().hex
        password_hash = self._hash_password(password, salt)
        self.users[username] = (password_hash, salt, 'user')

    def authenticate(self, username, password):
        if username not in self.users:
            return False
        stored_hash, salt, role = self.users[username]
        return stored_hash == self._hash_password(password, salt)

    def _hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 600000).hex()

    def authorize(self, username, required_role):
        if username not in self.users:
            return False
        _, _, role = self.users[username]
        return role == required_role

# Example usage
auth_service = UserAuthService()
auth_service.register_user("alice", os.getenv("ALICE_DEV_PASSWORD", "a_secure_default_password"))

assert auth_service.authenticate("alice", "alice_dev_password") == True
assert auth_service.authenticate("alice", "wrongpassword") == False
assert auth_service.authorize("alice", "user") == True