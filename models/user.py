from dataclasses import dataclass

@dataclass
class User:
    username: str
    password_hash: str
    role: str = "staff"

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password_hash"], data.get("role", "staff"))

class Admin(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "admin")

class Staff(User):
    def __init__(self, username, password_hash):
        super().__init__(username, password_hash, "staff")
