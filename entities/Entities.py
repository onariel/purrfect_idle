from Cat_counter import CatCounter
import json

class Entities:
    cps: float = 0
    cats: CatCounter
    entities_list: dict

    def __init__(self, cats: CatCounter) -> None:
        self.cats = cats
        self.entities_list = json.load(open('entities/Entities.json'))

    def update_cps(self) -> None:
        cps = self.cats

    def get_entities(self) -> dict:
        return self.entities_list