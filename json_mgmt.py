import json
from pathlib import Path

class JsonMGMT:
    SAVE_PATH = Path("data") / "save.json"
    DEFAULT_DATA = {
        "cats": {
            "cats": 0,
            "power": 0
        },
        "cats_seconds": {
            "cats": 0,
            "power": 0
        },
        "upgrades": [],
        "entities": []
    }

    def __init__(self):
        self.data = self.load_or_create()

    def load_or_create(self):
        if self.SAVE_PATH.exists():
            with open(self.SAVE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)

        data = self.DEFAULT_DATA.copy()
        self.save(data)
        return data

    def save(self, data=None):
        if data is None:
            data = self.data
        with open(self.SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def update(self, changes: dict, save: bool = True):
        for path, value in changes.items():
            keys = path.split(".")
            target = self.data
            for key in keys[:-1]:
                if key not in target or not isinstance(target[key], dict):
                    raise KeyError(f"Invalid path: '{path}' (missing '{key}')")
                target = target[key]

            last_key = keys[-1]
            if last_key not in target:
                raise KeyError(f"Invalid path: '{path}' (missing '{last_key}')")
            target[last_key] = value
        if save:
            self.save()

run = JsonMGMT()

run.update({"cats": {"cats": 15, "power": 3}})