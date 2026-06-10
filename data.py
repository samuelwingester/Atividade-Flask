import json
import os

class Data:
    data = None

    def __init__(self, dirpath = "storage", name = "biblioteca.json"):
        self.path = os.path.join(dirpath, name)

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        self.data = self.load()

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.data = data

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []