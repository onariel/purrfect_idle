

class CatCounter():
    cats = 0
    power_of_ten = 0
    cats_per_second = 0
    cats_per_second_power_of_ten = 0

    def __init__(self):
        pass

    def get_cats(self):
        return round(self.cats,3), self.power_of_ten

    def update_cats(self,time: int):
        # This formula calculates the number of cats made in a certain time. First you calculate the number of cats that a second of
        # cat per second will give if you remove the power of tens. Then you have to transform the time given in seconds and multiply the two
        self.cats += round((self.cats_per_second/(10**(self.power_of_ten - self.cats_per_second_power_of_ten))) * (time/1000),3)

        if self.cats // 1000 >= 1:
            self.cats = round(self.cats / 1000,3)
            self.power_of_ten += 3
        if self.cats < 1 and self.cats != 0:
            self.cats = round(self.cats * 1000,3)
            self.power_of_ten -= 3

    def update_cats_per_second(self,new_cats):
        self.cats_per_second += new_cats[0]/(10**(self.cats_per_second_power_of_ten - new_cats[1]))

        if self.cats_per_second // 1000 >= 1:
            self.cats_per_second = round(self.cats_per_second / 1000,3)
            self.cats_per_second_power_of_ten += 3

    def remove_cats(self,nb_cats):
        self.cats -= nb_cats[0]/(10**(self.cats_per_second_power_of_ten - nb_cats[1]))