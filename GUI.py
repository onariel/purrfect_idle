import tkinter as tk
from tkinter import ttk
from random import *
from Cat_counter import CatCounter
from entities.Entities import Entities


class GUI:
    cats: CatCounter
    entities: Entities
    window_width: int
    window_height: int
    window: tk.Tk
    clicker_column: tk.Frame
    information_column: ttk.Notebook
    upgrade_column: tk.Frame

    def init_with_save(self, cats: CatCounter) -> None:
        self.cats = cats
        self.init()

    def init_without_save(self) -> None:
        self.cats = CatCounter()
        self.init()

    def init(self) -> None:
        # The entities variable is a dict with every entities existing
        self.entities = Entities(self.cats)

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

        self.clicker_column = tk.Frame(self.window, bg="#F6C6D0")
        self.clicker_column.grid(row=0, column=0, sticky="nsew")

        self.information_column = ttk.Notebook(self.window)
        self.information_column.grid(row=0, column=1, sticky="nsew")

        entities_bought = tk.Frame(self.information_column, bg="#FFF3C4")  # light yellow
        statistics = tk.Frame(self.information_column, bg="#27F5A3")
        self.information_column.add(entities_bought, text="Game")
        self.information_column.add(statistics, text="Statistics")

        # Right column: upgrades
        self.upgrade_column = tk.Frame(self.window, bg="#C4E3F6")  # light blue
        self.upgrade_column.grid(row=0, column=2, sticky="nsew")

        self.init_upgrade_column()

        self.window.mainloop()

    def on_button(self, entity_name: str) -> None:
        print("you bought : ", entity_name)

    def init_upgrade_column(self) -> None:
        y = 0
        print(self.upgrade_column.winfo_width())

        for entity_name in self.entities.get_entities():
            frame = tk.Frame(self.upgrade_column, relief="groove", bd=2)
            frame.place(x=0, y=y, width=250, height=70)

            label = tk.Label(frame, text=entity_name)
            label.place(x=0, y=20, width=60, height=30)

            button = ttk.Button(frame, text="buy", command=lambda entity_name=entity_name: self.on_button(entity_name))
            button.place(x=100, y=20, width=80, height=30)
            y += 70


test = GUI()
test.init_without_save()

# OLD - keep for now as temporary if needed
# TO BE CLEAN LATER
# def launch():
#
#     # Initialisation of important classes
#     cats = CatCounter()
#     entities = Entities(cats)
#
#     colors = ['#3f2e4f', '#77d584', '#0eb0de', '#ef38a1', '#d8c8a2']
#     # Root Window
#     root = tk.Tk()
#     root.title("Purrfect Idle")
#     root.geometry("1080x720")
#
#     # Three columns: sides = 1 part each, center = 3 parts
#     root.columnconfigure(0, weight=1, uniform="cols")
#     root.columnconfigure(1, weight=3, uniform="cols")
#     root.columnconfigure(2, weight=1, uniform="cols")
#     root.rowconfigure(0, weight=1)
#
#     # Left column: clicker
#     clicker = tk.Frame(root, bg="#F6C6D0")  # pink
#     clicker.grid(row=0, column=0, sticky="nsew")
#
#     # Center column: tabs
#     nav = ttk.Notebook(root)
#     nav.grid(row=0, column=1, sticky="nsew")
#
#     frame1 = tk.Frame(nav, bg="#FFF3C4")  # light yellow
#     frame2 = tk.Frame(nav, bg="#27F5A3")
#     nav.add(frame1, text="Game")
#     nav.add(frame2, text="Statistics")
#
#     # Right column: upgrades
#     upgrades = tk.Frame(root, bg="#C4E3F6")  # light blue
#     upgrades.grid(row=0, column=2, sticky="nsew")
#
#     # Label inside column
#     nb_of_cats = tk.Label(clicker, text=str(cats.get_cats()[0]) + "*10**" + str(cats.get_cats()[1]))
#     nb_of_cats.place(x=170, y=170)
#
#     def updates():
#         cats.update_cats(100)
#         nb_of_cats.config(text=str(cats.get_cats()[0]) + "*10**" + str(cats.get_cats()[1]))
#         #cats.update_cats_per_second([1,0])
#         #color = colors[randint(0, 4)]
#         #clicker.config(bg=color)
#         clicker.after(100, updates)
#         print(clicker.winfo_width(), clicker.winfo_height())
#
#
#     updates()
#
#     root.mainloop()
