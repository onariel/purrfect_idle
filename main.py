from GUI import *
from json_mgmt import *


def main():
    data = JsonMGMT().data
    run = GUI(data)


if __name__ == '__main__':
    main()
