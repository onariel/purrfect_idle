from GUI import *
from json_mgmt import *


def main():
    run = GUI()

    if JsonMGMT.SAVE_PATH.exists():
        data = JsonMGMT().data

        cats = CatCounter()
        cats.cats = data["cats"]["cats"]
        cats.power_of_ten = data["cats"]["power"]
        cats.cats_per_second = data["cats_seconds"]["cats"]
        cats.cats_per_second_power_of_ten = data["cats_seconds"]["power"]

        run.init_with_save(cats)
    else:
        run.init_without_save()


if __name__ == '__main__':
    main()
