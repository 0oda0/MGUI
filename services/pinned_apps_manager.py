# services/pinned_apps_manager.py
import json
import os

class PinnedAppsManager:
    def __init__(self, storage_file="pinned_apps.json"):
        self.storage_file = storage_file
        self.apps = self.load()

    def load(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.apps, f, indent=2, ensure_ascii=False)

    def add(self, name, path):
        self.apps.append({"name": name, "path": path})
        self.save()

    def remove(self, path):
        self.apps = [app for app in self.apps if app["path"] != path]
        self.save()

    def get_all(self):
        return self.apps