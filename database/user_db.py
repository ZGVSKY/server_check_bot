import json
import os
from typing import Dict, Any, Optional

DB_PATH = "database/users.json"

class UserDB:
    def __init__(self):
        os.makedirs("database", exist_ok=True)
        if not os.path.exists(DB_PATH):
            self.users = {}
            self.save()
        else:
            self.load()

    def load(self):
        with open(DB_PATH, "r", encoding="utf-8") as f:
            self.users = json.load(f)

    def save(self):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(str(user_id))

    def set_permission(self, user_id: str, permission: str, username: str = "Unknown"):
        # permissions: "unauthorized", "stats_only", "full"
        self.users[str(user_id)] = {
            "permission": permission,
            "username": username
        }
        self.save()

    def get_all_users(self) -> Dict[str, Any]:
        return self.users

user_db = UserDB()
