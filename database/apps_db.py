import json
import os
from typing import Dict, List

APPS_DB_PATH = "database/apps.json"

class AppsDB:
    def __init__(self):
        os.makedirs("database", exist_ok=True)
        if not os.path.exists(APPS_DB_PATH):
            self.apps = []
            self.save()
        else:
            self.load()

    def load(self):
        with open(APPS_DB_PATH, "r", encoding="utf-8") as f:
            self.apps = json.load(f)

    def save(self):
        with open(APPS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.apps, f, indent=4, ensure_ascii=False)

    def add_app(self, name: str, path: str):
        self.apps.append({"name": name, "path": path})
        self.save()

    def get_apps(self) -> List[Dict[str, str]]:
        return self.apps

    def remove_app(self, index: int):
        if 0 <= index < len(self.apps):
            self.apps.pop(index)
            self.save()

apps_db = AppsDB()
