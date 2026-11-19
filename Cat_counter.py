import json
from entities.Entities import Entities
from convert.convert import Convert

class CatCounter:
    rounded_to = 12
    price_augmentation = 1.05 # 5% augmentation in price each time you buy an item

    cats: float
    power_of_ten: int

    cats_per_seconds: float
    cats_per_seconds_power_of_ten: int

    cats_per_click: float
    cats_per_click_power_of_ten: int

    """
    The entities bought will be a dictionary that links an entity type to, amount of entities bought, price, flat cps, and modifier in %. Example:
    entities_bought = {
        "grandma" : {
            "amount_bought" : 5
            "flat_cps" : 10
            "flat_cps_power_of_ten" : 0
            "modifier_cps" : 5,
            "price" : 100,
            "price_power_of_ten" : 0
            }
        }
    in this example we have 5 grandma that gives 5*((10*10**0)+(10*0.05)) = 52.5 cps, and it costs 100 cats
    """
    entities_bought: dict
    """This global modifier will apply to total cps"""
    global_modifier: float
    entities_list: dict

    def __init__(self, save: dict) -> None:
        self.cats = save["cats"]["cats"]
        self.power_of_ten = save["cats"]["power_of_ten"]

        self.cats_per_seconds = save["cats_per_seconds"]["cats"]
        self.cats_per_seconds_power_of_ten = save["cats_per_seconds"]["power_of_ten"]

        self.cats_per_click = save["cats_per_click"]["cats"]
        self.cats_per_click_power_of_ten = save["cats_per_click"]["power_of_ten"]

        self.init_entities(save)
        self.global_modifier = save["global_modifier"]


    def init_entities(self, save : dict) -> None:
        self.entities_bought = save["entities"]
        self.entities_list = Entities.get_entities()
        for entity_key in self.entities_list:
            if entity_key not in self.entities_bought:
                entity = self.entities_list[entity_key]
                self.entities_bought[entity_key] = {
                    "amount_bought": 0,
                    "flat_cps": entity["cps"],
                    "flat_cps_power_of_ten": entity["cps_power_of_ten"],
                    "modifier_cps": 0,
                    "price" : entity["price"],
                    "price_power_of_ten" : entity["price_power_of_ten"]
            }

    def get_entity_info(self, entity_name: str) -> dict:
        return self.entities_bought[entity_name]

    def get_cats(self) -> str:
        return Convert.convert(self.cats, self.power_of_ten)

    def get_cats_per_second(self) -> str:
        return Convert.convert(self.cats_per_seconds, self.cats_per_seconds_power_of_ten)

    def get_entities_bought(self) -> dict:
        return self.entities_bought

    def add_entity(self, entity_name: str) -> None:
        self.entities_bought[entity_name]["amount_bought"] += 1
        future_price = self.entities_bought[entity_name]["price"] * self.price_augmentation
        if future_price > 1000:
            self.entities_bought[entity_name]["price_power_of_ten"] += 3
            self.entities_bought[entity_name]["price"] = round(self.entities_bought[entity_name]["price"]/1000, self.rounded_to)
        self.entities_bought[entity_name]["price"] *= self.price_augmentation
        self.update_cats_per_second()

        if self.power_of_ten - self.entities_bought[entity_name]["price_power_of_ten"] < self.rounded_to:
            self.cats -= self.entities_bought[entity_name]["price"] * (10** (self.entities_bought[entity_name]["price_power_of_ten"] - self.power_of_ten))

    def is_boughtable(self, entity_name: str) -> bool:
        entity = self.entities_bought[entity_name]
        if self.power_of_ten > entity["price_power_of_ten"]:
            return True
        elif self.power_of_ten == entity["price_power_of_ten"]:
            if self.cats > entity["price"]:
                return True
        return False

    def update_cats(self, time: int) -> str:
        # This formula calculates the number of cats made in a certain time. First you calculate the number of cats that a second of
        # cat per second will give if you remove the power of tens. Then you have to transform the time given in seconds and multiply the two
        self.cats += round(
            (self.cats_per_seconds / (10 ** (self.power_of_ten - self.cats_per_seconds_power_of_ten))) * (time / 1000),
            self.rounded_to)

        if self.cats > 1000:
            self.cats = round(self.cats / 1000, self.rounded_to)
            self.power_of_ten += 3
        if self.cats < 1 and self.cats != 0:
            self.cats = round(self.cats * 1000, self.rounded_to)
            self.power_of_ten -= 3

        new_cats_power_of_ten = self.cats_per_seconds_power_of_ten
        while time >= 1000:
            new_cats_power_of_ten += 3
            time /= 1000

        return Convert.convert(self.cats_per_seconds * (time/1000),new_cats_power_of_ten)

    def update_cats_per_second(self) -> None:
        new_cats_per_seconds = self.cats_per_seconds
        new_cats_per_seconds_power_of_ten = self.cats_per_seconds_power_of_ten
        for entity_key in self.entities_bought:
            entity = self.entities_bought[entity_key]
            entity_calculated_cps = entity["amount_bought"] * entity["flat_cps"] + (
                        entity["amount_bought"] * entity["flat_cps"] * entity["modifier_cps"])
            entity_calculated_cps_power_of_ten = entity["flat_cps_power_of_ten"]

            while entity_calculated_cps > 1000:
                entity_calculated_cps = round(entity_calculated_cps / 1000, self.rounded_to)
                entity_calculated_cps_power_of_ten += 3

            if new_cats_per_seconds_power_of_ten - entity_calculated_cps_power_of_ten < self.rounded_to:
                new_cats_per_seconds += entity_calculated_cps * 10 ** (
                            entity_calculated_cps_power_of_ten - new_cats_per_seconds_power_of_ten)

            if new_cats_per_seconds > 1000:
                new_cats_per_seconds = round(new_cats_per_seconds / 1000, self.rounded_to)
                new_cats_per_seconds_power_of_ten += 3

        new_cats_per_seconds += new_cats_per_seconds * self.global_modifier
        if new_cats_per_seconds > 1000:
            new_cats_per_seconds = round(new_cats_per_seconds / 1000, self.rounded_to)
            new_cats_per_seconds_power_of_ten += 3

        self.cats_per_seconds = new_cats_per_seconds - (self.cats_per_seconds * 10 ** (
                    self.cats_per_seconds_power_of_ten - new_cats_per_seconds_power_of_ten))
        self.cats_per_seconds_power_of_ten = new_cats_per_seconds_power_of_ten

    def get_cats_per_click(self) -> str:
        return Convert.convert(self.cats_per_click,self.cats_per_click_power_of_ten)

    def add_cats(self, nb_cats: tuple) -> None:
        self.cats += round(nb_cats[0] * (10 ** (nb_cats[1] - self.power_of_ten)), self.rounded_to)

        while self.cats / 1000 >= 1:
            self.cats = round(self.cats / 1000, self.rounded_to)
            self.power_of_ten += 3

    def remove_cats(self, nb_cats: tuple) -> None:
        self.cats -= round(nb_cats[0] * (10 ** (nb_cats[1] - self.power_of_ten)), self.rounded_to)

        while 0 < self.cats < 1:
            self.cats = round(self.cats * 1000, self.rounded_to)
            self.power_of_ten -= 3

    def click(self) -> None:
        self.cats += round(self.cats_per_click * (10 ** (self.cats_per_click_power_of_ten - self.power_of_ten)),
                           self.rounded_to)

    def save_cats_info(self) -> dict:
        return {
            "cats.cats": self.cats,
            "cats.power_of_ten": self.power_of_ten,
            "cats_per_seconds.cats": self.cats_per_seconds,
            "cats_per_seconds.power_of_ten": self.cats_per_seconds_power_of_ten,
            "cats_per_click.cats": self.cats_per_click,
            "cats_per_click.power_of_ten": self.cats_per_click_power_of_ten,
        }
