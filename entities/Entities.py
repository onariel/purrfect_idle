import json


class Entities:

    @staticmethod
    def get_entities() -> dict:
        return json.load(open('entities/Entities.json'))
