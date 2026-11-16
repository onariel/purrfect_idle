class CatCounter:
    cats: float
    power_of_ten: int

    cats_per_second: float
    cats_per_second_power_of_ten: int

    cats_per_click: float
    cats_per_click_power_of_ten: int

    def __init__(self, save: dict) -> None:
        self.cats = save["cats"]["cats"]
        self.power_of_ten = save["cats"]["power_of_ten"]

        self.cats_per_second = save["cats_per_seconds"]["cats"]
        self.cats_per_second_power_of_ten = save["cats_per_seconds"]["power_of_ten"]

        self.cats_per_click = save["cats_per_click"]["cats"]
        self.cats_per_click_power_of_ten = save["cats_per_click"]["power_of_ten"]

    def get_cats(self) -> tuple:
        return round(self.cats, 3), self.power_of_ten

    def get_cats_per_second(self) -> tuple:
        return round(self.cats_per_second, 3), self.cats_per_second_power_of_ten

    def update_cats(self, time: int) -> None:
        # This formula calculates the number of cats made in a certain time. First you calculate the number of cats that a second of
        # cat per second will give if you remove the power of tens. Then you have to transform the time given in seconds and multiply the two
        self.cats += round(
            (self.cats_per_second / (10 ** (self.power_of_ten - self.cats_per_second_power_of_ten))) * (time / 1000),
            12)

        if self.cats / 1000 >= 1:
            self.cats = round(self.cats / 1000, 12)
            self.power_of_ten += 3
        if self.cats < 1 and self.cats != 0:
            self.cats = round(self.cats * 1000, 12)
            self.power_of_ten -= 3

    def update_cats_per_second(self, new_cats: tuple) -> None:
        self.cats_per_second += new_cats[0] / (10 ** (self.cats_per_second_power_of_ten - new_cats[1]))

        if self.cats_per_second // 1000 >= 1:
            self.cats_per_second = round(self.cats_per_second / 1000, 12)
            self.cats_per_second_power_of_ten += 3

    def get_cats_per_click(self) -> tuple:
        return round(self.cats_per_click, 3), self.cats_per_click_power_of_ten

    def add_cats(self, nb_cats: tuple) -> None:
        self.cats += round(nb_cats[0] * (10 ** (nb_cats[1] - self.power_of_ten)), 12)

        while self.cats / 1000 >= 1:
            self.cats = round(self.cats / 1000, 12)
            self.power_of_ten += 3

    def remove_cats(self, nb_cats: tuple) -> None:
        self.cats -= round(nb_cats[0] * (10 ** (nb_cats[1] - self.power_of_ten)), 12)

        while 0 < self.cats < 1:
            self.cats = round(self.cats * 1000, 12)
            self.power_of_ten -= 3

    def click(self) -> None:
        self.cats += round(self.cats_per_click * (10 ** (self.cats_per_click_power_of_ten - self.power_of_ten)), 12)

    def save_cats_info(self) -> dict:
        return {
            "cats.cats": self.cats,
            "cats.power_of_ten": self.power_of_ten,
            "cats_per_seconds.cats": self.cats_per_second,
            "cats_per_seconds.power_of_ten": self.cats_per_second_power_of_ten,
            "cats_per_click.cats": self.cats_per_click,
            "cats_per_click.power_of_ten": self.cats_per_click_power_of_ten,
        }
