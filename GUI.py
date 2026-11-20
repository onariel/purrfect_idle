import tkinter as tk
from tkinter import ttk
from Cat_counter import CatCounter
from entities.Entities import Entities
from json_mgmt import JsonMGMT
from minigames.minigames import Minigames
from graph import Graph
from Statistics import Statistics
from convert.convert import Convert
from Report import Report


class GUI:
    cats: CatCounter
    window_width: int
    window_height: int
    window: tk.Tk
    clicker_column: tk.Frame
    information_column: ttk.Notebook
    upgrade_column: tk.Frame

    entities_frame: dict

    """
    Main GUI
    """

    def __init__(self, save: JsonMGMT) -> None:
        """Initialize the GUI """
        self.save = save
        self.cats = CatCounter(save.data)
        # The entities variable is a dict with every entity existing*
        self.minigames = Minigames()
        self.report = Report(self.cats, self.save)

        # Initializing the window
        self.window = tk.Tk()
        self.window_width = 720
        self.window_height = 1080
        self.window.title("Purrfect Idle")
        self.window.geometry(str(self.window_height) + "x" + str(self.window_width))

        # Three columns: sides = 1 part each, center = 3 parts
        self.window.columnconfigure(0, weight=1, uniform="cols")
        self.window.columnconfigure(1, weight=3, uniform="cols")
        self.window.columnconfigure(2, weight=1, uniform="cols")
        self.window.rowconfigure(0, weight=1)

        self.clicker_column = tk.Frame(self.window)
        self.clicker_column.grid(row=0, column=0, sticky="nsew")

        self.information_column = ttk.Notebook(self.window)
        self.information_column.grid(row=0, column=1, sticky="nsew")

        self.entities_bought = tk.Frame(self.information_column)
        self.statistics = tk.Frame(self.information_column)

        # Right column: upgrades
        self.upgrade_column = tk.Frame(self.window)
        self.upgrade_column.grid(row=0, column=2, sticky="nsew")

        self.init_upgrade_column()
        self.init_main_column()
        self.init_clicker_column()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.autosave()

        self.window.mainloop()

    def save_file(self) -> None:
        new_save = self.cats.save_cats_info()
        self.save.update(new_save)

    def autosave(self) -> None:
        """Autosave every minutes"""
        self.save_file()
        self.window.after(10000, self.autosave)

    def on_close(self) -> None:
        self.save_file()
        self.window.destroy()

    """
    Clicker Column
    """

    def init_clicker_column(self) -> None:
        self.clicker_column.columnconfigure(0, weight=1)

        label_cat = tk.Label(self.clicker_column)
        label_cat.grid(row=0, column=0, pady=10)

        label_cat_seconds = tk.Label(self.clicker_column)
        label_cat_seconds.grid(row=1, column=0, pady=10)

        button_clicker = ttk.Button(self.clicker_column, text='Click Me !!',
                                    command=self.on_button_clicker_column)
        button_clicker.grid(row=2, column=0, pady=10)

        self.update_clicker_column(label_cat, label_cat_seconds)

    def update_clicker_column(self, label_cat: tk.Label, label_cat_seconds : tk.Label) -> None:
        self.cats.update_cats(50)  # 50 ms
        nb_cats = self.cats.get_cats()
        nb_cats_per_seconds = self.cats.get_cats_per_second()
        label_cat.config(text=str(nb_cats) + " cats")
        label_cat_seconds.config(text=str(nb_cats_per_seconds) + " cats per seconds")
        label_cat.after(50, self.update_clicker_column, label_cat, label_cat_seconds)


    def on_button_clicker_column(self):
        self.cats.click()

    """
    Main Column
    """

    def init_main_column(self) -> None:
        self.information_column.add(self.entities_bought, text="Game")
        self.information_column.add(self.statistics, text="Statistics")

        self.init_game_section()
        self.init_stats_section()

    def init_game_section(self) -> None:
        self.entities_bought.columnconfigure(0, weight=1)

        frame = tk.Frame(self.entities_bought)
        frame.grid(row=0, column=0, sticky="nsew", padx=10)
        frame.columnconfigure(0, weight=1)

        title_label = tk.Label(frame, text="Minigames to play in order to gain more cats !")
        title_label.grid(row=0, column=0, pady=10)

        for row, game in enumerate(self.minigames.get_minigames()):
            card = tk.Frame(frame, relief="groove", bd=2)
            card.grid(row=row + 1, column=0, sticky="ew", pady=5)
            card.columnconfigure(0, weight=1)

            name_label = tk.Label(card, text=game.NAME, anchor="w", font=("TkDefaultFont", 11, "bold"))
            name_label.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))

            button = ttk.Button(card, text="Play",
                                command=lambda minigame=game: self.open_minigame(minigame))
            button.grid(row=0, column=1, rowspan=2, sticky="e", padx=5, pady=5)

    def init_stats_section(self) -> None:
        self.statistics.columnconfigure(0, weight=1)

        frame = tk.Frame(self.statistics)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)

        title_label = tk.Label(frame, text="You can view here the statistics of your game.")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        graph_btn = tk.Button(frame, text="Open the Cat graph", command=lambda: self.graph_cats())
        graph_btn.grid(row=1, column=0, sticky="w", pady=10)

        export_btn = tk.Button(frame, text="Export", command=lambda: self.export_stats())
        export_btn.grid(row=1, column=1, pady=10, sticky="e")

        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        Statistics(frame, self.save, self.cats, 2)

    def export_stats(self) -> None:
        self.report.export()

    def open_minigame(self, minigame) -> None:
        minigame(self.window, self.cats, self.save)

    def graph_cats(self) -> None:
        # Use to display some graphs via Matplotlib (can be multiple graphs via notebook)
        # Sone graph ideas:
        # - Cats per second from each entity (bar chart)
        # - total cps over time (need to implement a time in the save)
        # - minigame graphs (Win/loss/draw ratio)
        Graph(self.window, self.cats, self.save)

    """
    Upgrade Column
    """

    def on_button_upgrade_column(self,event, entity_name: str) -> None:
        if self.entities_frame[entity_name]["is_buyable"]:
            self.cats.add_entity(entity_name)

    def init_upgrade_column(self) -> None:
        # One full-width row per entity, stacked from the top of the column
        self.upgrade_column.columnconfigure(0, weight=1)
        entities = Entities.get_entities()
        self.entities_frame = {}
        for row, entity_name in enumerate(entities):
            self.entities_frame[entity_name] = {}
            frame = tk.Frame(self.upgrade_column, relief="groove", bd=2)
            frame.grid(row=row, column=0, sticky="ew")
            frame.columnconfigure(0, weight=1)
            frame.bind("<Button-1>", lambda event="oui", entity_name=entity_name: self.on_button_upgrade_column(event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["frame"] = frame

            name_entity = entities[entity_name]["name"]
            label_entity_name = tk.Label(frame, text=name_entity[:15] + "..." if len(name_entity) > 15 else name_entity, anchor="w")
            label_entity_name.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
            label_entity_name.bind("<Button-1>", lambda event="oui", entity_name=entity_name: self.on_button_upgrade_column(event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["name"] = label_entity_name


            label_entity_quantity = tk.Label(frame, text="quantity", anchor="w")
            label_entity_quantity.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            label_entity_quantity.bind("<Button-1>", lambda event="oui", entity_name=entity_name: self.on_button_upgrade_column(event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["quantity"] = label_entity_quantity

            label_entity_price = tk.Label(frame, text=str(entities[entity_name]["price"]) + " cats", anchor="w")
            label_entity_price.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
            label_entity_price.bind("<Button-1>", lambda event="oui", entity_name=entity_name: self.on_button_upgrade_column(event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["price"] = label_entity_price
        self.update_upgrade_column()

    def update_upgrade_column(self) -> None:
        entities = Entities.get_entities()
        for entity_key in entities:
            entity = self.cats.get_entity_info(entity_key)
            quantity_label : tk.Label = self.entities_frame[entity_key]["quantity"]
            quantity_label.config(text=entity["amount_bought"])

            price_label : tk.Label = self.entities_frame[entity_key]["price"]
            price_label.config(text=str(Convert.convert(entity["price"], entity["price_power_of_ten"]) + " cats"))

            name_label : tk.Label = self.entities_frame[entity_key]["name"]

            frame: tk.Frame = self.entities_frame[entity_key]["frame"]
            if self.cats.is_buyable(entity_key):
                frame.config(bg="#C8EACB")
                quantity_label.config(bg="#C8EACB")
                price_label.config(bg="#C8EACB")
                name_label.config(bg="#C8EACB")
                self.entities_frame[entity_key]["is_buyable"] = True
            else:
                frame.config(bg="#ff9b9b")
                quantity_label.config(bg="#ff9b9b")
                price_label.config(bg="#ff9b9b")
                name_label.config(bg="#ff9b9b")
                self.entities_frame[entity_key]["is_buyable"] = False



        quantity_label.after(100, self.update_upgrade_column)

