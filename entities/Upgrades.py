import json
from entities.Entities import Entities
from Json_MGMT import JsonMGMT

class Upgrades():

    @staticmethod
    def get_upgrades(save : JsonMGMT) -> list:
        upgrades_list = []
        upgrades_bought = save.data["upgrades"]
        upgrades = json.load(open('entities/Upgrades.json'))
        for upgrade in upgrades:
            if not upgrade["name"] in upgrades_bought:
                upgrades_list.append(upgrade)

        upgrades_list.sort(key=lambda x: x["price_power_of_ten"])
        j = 0
        for i in range(1,len(upgrades_list)):
            if not upgrades_list[i]["price_power_of_ten"] == upgrades_list[i-1]["price_power_of_ten"]:
                upgrades_list[j:i] = sorted(upgrades_list[j:i], key=lambda x: x["price"])
                j = i
        return upgrades_list