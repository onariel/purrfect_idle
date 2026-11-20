from minigames.tic_tac_toe import TicTacToe
import tkinter as tk
from tkinter import ttk
from Cat_counter import CatCounter
from json_mgmt import JsonMGMT


class Minigames:
    minigames: list
    cards: dict

    def __init__(self) -> None:
        self.minigames = [TicTacToe]
        self.cards = {}
        self.temp_label = None

    def init_game_section(self, parent: tk.Frame, window: tk.Tk, cats: CatCounter, save: JsonMGMT) -> None:
        self.window = window
        self.cats = cats
        self.save = save

        parent.columnconfigure(0, weight=1)

        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=10)
        self.frame.columnconfigure(0, weight=1)

        title_label = tk.Label(self.frame, text="Minigames to play in order to gain more cats !")
        title_label.grid(row=0, column=0, pady=10)

        self.update_window()

    def add_card(self, row: int, game) -> None:
        card = tk.Frame(self.frame, relief="groove", bd=2)
        card.grid(row=row + 1, column=0, sticky="ew", pady=5)
        card.columnconfigure(0, weight=1)

        name_label = tk.Label(card, text=game.NAME, anchor="w", font=("TkDefaultFont", 11, "bold"))
        name_label.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))

        button = ttk.Button(card, text="Play",
                            command=lambda minigame=game: minigame(self.window, self.cats, self.save))
        button.grid(row=0, column=1, rowspan=2, sticky="e", padx=5, pady=5)

        self.cards[game] = card

    def update_window(self) -> None:
        # Render the card of every minigame whose parent entity has been bought since the last check
        for row, game in enumerate(self.minigames):
            if game not in self.cards and self.cats.get_entity_info(game.PARENT_ENTITY)["amount_bought"] > 0:
                self.add_card(row, game)

        # Show the hint once while no minigame is unlocked, and remove it as soon as one is
        minigame_bought: bool = len(self.cards) > 0
        if minigame_bought and self.temp_label is not None:
            self.temp_label.destroy()
            self.temp_label = None
        elif not minigame_bought and self.temp_label is None:
            self.temp_label = tk.Label(self.frame, text="Buy at least one entity to unlock its minigame.")
            self.temp_label.grid(row=1, column=0, sticky="ew")

        self.frame.after(100, self.update_window)

    def get_minigames(self) -> list:
        return self.minigames

    def get_number_of_minigames(self) -> int:
        return len(self.minigames)
