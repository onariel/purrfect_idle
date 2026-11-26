import copy
import json
from pathlib import Path
import datetime as dt


class JsonMGMT:
    SAVE_PATH = Path("data") / "save.json"
    TIMESTAMP_FORMAT = "%Y-%m-%d-%H:%M:%S"
    MAX_CATS_HISTORY = 500
    DEFAULT_DATA = {
        "cats": {
            "cats": 0,
            "power_of_ten": 0
        },
        "cats_per_seconds": {
            "cats": 0,
            "power_of_ten": 0
        },
        "cats_per_click": {
            "cats": 1,
            "power_of_ten": 0
        },
        "nyancat_clicked": 0,
        "upgrades": [],
        "entities": {},
        "minigames": {
            "tictactoe": {
                "win": 0,
                "tie": 0,
                "lose": 0
            }
        },
        "global_modifier": 0,
        "total_cats": {
            "cats": 0,
            "power_of_ten": 0
        },
        "all_time_cats": []
    }

    def __init__(self):
        self.data = self.load_or_create()

    def load_or_create(self):
        if self.SAVE_PATH.exists():
            with open(self.SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Older saves miss the keys added since: fill them with their default value
            for key, default in self.DEFAULT_DATA.items():
                data.setdefault(key, copy.deepcopy(default))
            return data

        data = copy.deepcopy(self.DEFAULT_DATA)
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

    def add_all_time_cats(self, cats: float, power_of_ten: int, save: bool = True) -> None:
        history = self.data.setdefault("all_time_cats", [])
        if not isinstance(history, list):  # old saves stored a dict
            history = self.data["all_time_cats"] = []

        history.append({
            "timestamp": dt.datetime.now().strftime(self.TIMESTAMP_FORMAT),
            "cats": cats,
            "power_of_ten": power_of_ten
        })
        del history[:-self.MAX_CATS_HISTORY]  # keep only the newest entries

        if save:
            self.save()