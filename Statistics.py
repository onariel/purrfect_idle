import tkinter as tk
from Cat_counter import CatCounter
from json_mgmt import JsonMGMT
from minigames.minigames import Minigames


class Statistics:

    def __init__(self, parent: tk.Frame, save: JsonMGMT, cats: CatCounter, row: int) -> None:
        self.parent = parent
        self.save = save
        self.cats = cats
        self.row = row
        self.games = Minigames()

        self.entities_labels = {}
        self.minigames_labels = {}

        self.cats_stats()
        self.entities_stats()
        self.minigame_stats_init()

        self.update_stats()

    def cats_stats(self) -> None:
        cats_section_label = tk.Label(self.parent, text="Cats Statistics")
        cats_section_label.grid(row=self.row + 1, column=0, columnspan=2, sticky="ew")

        total_cats_label = tk.Label(self.parent, text="Total Cat Count: ")
        total_cats_label.grid(row=self.row + 2, column=0, sticky="w")

        cats_per_seconds_label = tk.Label(self.parent, text="Cat per Second: ")
        cats_per_seconds_label.grid(row=self.row + 3, column=0, sticky="w")

        cats_per_clicks_label = tk.Label(self.parent, text="Cat per Clicks: ")
        cats_per_clicks_label.grid(row=self.row + 4, column=0, sticky="w")

        self.total_cats_value = tk.Label(self.parent)
        self.total_cats_value.grid(row=self.row + 2, column=1, sticky="e")

        self.cats_per_seconds_value = tk.Label(self.parent)
        self.cats_per_seconds_value.grid(row=self.row + 3, column=1, sticky="e")

        self.cats_per_clicks_value = tk.Label(self.parent)
        self.cats_per_clicks_value.grid(row=self.row + 4, column=1, sticky="e")

    def entities_stats(self) -> None:
        entities_section_label = tk.Label(self.parent, text="Entities Statistics")
        entities_section_label.grid(row=self.row + 5, column=0, columnspan=2, sticky="ew")

        frame = tk.Frame(self.parent)
        frame.grid(row=self.row + 6, column=0, columnspan=2, sticky="nsew")
        for column in range(3):
            frame.columnconfigure(column, weight=1, uniform="entities")

        entiny_name_label = tk.Label(frame, text="Entities: ")
        entiny_name_label.grid(row=0, column=0, sticky="w")

        entity_qtt_label = tk.Label(frame, text="Quantity: ")
        entity_qtt_label.grid(row=0, column=1)

        entity_cps_label = tk.Label(frame, text="Cumulative Productions: ")
        entity_cps_label.grid(row=0, column=2, sticky="e")

        for row, entity_name in enumerate(self.save.data["entities"]):
            label_entity_name = tk.Label(frame, text=entity_name)
            label_entity_name.grid(row=row + 1, column=0, sticky="w")

            label_entity_quantity = tk.Label(frame)
            label_entity_quantity.grid(row=row + 1, column=1, sticky="ew")

            label_entity_cps = tk.Label(frame)
            label_entity_cps.grid(row=row + 1, column=2, sticky="e")

            self.entities_labels[entity_name] = (label_entity_quantity, label_entity_cps)

    def minigame_stats_init(self) -> None:
        minigames_section_label = tk.Label(self.parent, text="Minigames Statistics")
        minigames_section_label.grid(row=self.row + 11, column=0, columnspan=2, sticky="ew")

        frame = tk.Frame(self.parent)
        frame.grid(row=self.row + 12, column=0, columnspan=2, sticky="nsew")
        for column in range(3):
            frame.columnconfigure(column, weight=1, uniform="minigames")

        for i, game in enumerate(self.games.get_minigames()):
            self.load_minigame_stats(frame, game, i // 3, i % 3)

    def load_minigame_stats(self, parent: tk.Frame, minigame, row: int, column: int) -> None:
        key = minigame.NAME.lower().replace(" ", "")

        cell = tk.Frame(parent)
        cell.grid(row=row, column=column, sticky="nsew")

        game_name = tk.Label(cell, text=minigame.NAME)
        game_name.grid(row=0, column=0, columnspan=2)

        win_label = tk.Label(cell, text="Wins: ")
        win_label.grid(row=1, column=0, sticky="w")
        tie_label = tk.Label(cell, text="Ties: ")
        tie_label.grid(row=2, column=0, sticky="w")
        lose_label = tk.Label(cell, text="Loses: ")
        lose_label.grid(row=3, column=0, sticky="w")

        win_score = tk.Label(cell)
        win_score.grid(row=1, column=1)
        tie_score = tk.Label(cell)
        tie_score.grid(row=2, column=1)
        lose_score = tk.Label(cell)
        lose_score.grid(row=3, column=1)

        self.minigames_labels[key] = (win_score, tie_score, lose_score)

    def update_stats(self) -> None:
        """Refresh every displayed value, every 500 ms"""
        nb_cats = self.cats.get_cats()
        self.total_cats_value.config(text=nb_cats)

        nb_cats_per_seconds = self.cats.get_cats_per_second()
        self.cats_per_seconds_value.config(text=nb_cats_per_seconds)

        nb_cats_per_click = self.cats.get_cats_per_click()
        self.cats_per_clicks_value.config(text=nb_cats_per_click)

        for entity_name, (label_quantity, label_cps) in self.entities_labels.items():
            entity = self.save.data["entities"][entity_name]
            label_quantity.config(text=entity["amount_bought"])
            label_cps.config(text=f"{entity['flat_cps']}*10**{entity['flat_cps_power_of_ten']}")

        for key, (win_score, tie_score, lose_score) in self.minigames_labels.items():
            stats = self.save.data["minigames"][key]
            win_score.config(text=stats["win"])
            tie_score.config(text=stats["tie"])
            lose_score.config(text=stats["lose"])

        self.parent.after(500, self.update_stats)
