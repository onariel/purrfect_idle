from minigames.tic_tac_toe import TicTacToe


class Minigames:
    minigames: list

    def __init__(self):
        self.minigames = [TicTacToe]

    def get_minigames(self) -> list:
        return self.minigames

    def get_number_of_minigames(self) -> int:
        return len(self.minigames)
