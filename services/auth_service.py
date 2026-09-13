from models.user import User, Admin, Staff
from utils.storage import load_json, save_json
from utils.security import hash_password, verify_password

class AuthService:
    FILE = "users.json"

    def __init__(self):
        self.users = [User.from_dict(x) for x in load_json(self.FILE)]
        if not self.users:
            self.register("admin", "admin123", "admin")

    def _save(self):
        save_json(self.FILE, [u.to_dict() for u in self.users])

    def register(self, username, password, role="staff"):
        if any(u.username.lower() == username.lower() for u in self.users):
            raise ValueError("Username already exists.")
        if role == "admin":
            user = Admin(username, hash_password(password))
        else:
            user = Staff(username, hash_password(password))
        self.users.append(user)
        self._save()
        return user

    def login(self, username, password):
        user = next((u for u in self.users if u.username.lower() == username.lower()), None)
        if user and verify_password(password, user.password_hash):
            return user
        return None
