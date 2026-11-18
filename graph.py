from Cat_counter import CatCounter
import tkinter as tk
from tkinter import ttk
from json_mgmt import JsonMGMT
from minigames.minigames import Minigames
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph:

    def __init__(self, window: tk.Tk, cats: CatCounter, save: JsonMGMT) -> None:
        self.cats = cats
        self.save = save
        self.games = Minigames()

        self.popup = tk.Toplevel(window)
        self.popup.title("Graphs")
        self.popup.transient(window)
        self.popup.geometry("800x800")

        self.popup.columnconfigure(0, weight=1, uniform="cols")
        self.popup.rowconfigure(0, weight=1)

        self.page = ttk.Notebook(self.popup)
        self.page.grid(row=0, column=0, sticky="nsew")

        self.minigames_ratio = tk.Frame(self.page)
        self.graph2 = tk.Frame(self.page)

        self.init_notebook()

    def init_notebook(self) -> None:
        self.page.add(self.minigames_ratio, text="Minigames Ratio")
        self.page.add(self.graph2, text="Graph2")

        self.init_minigames_ratio()

    def init_minigames_ratio(self) -> None:
        self.minigames_ratio.columnconfigure(0, weight=1)

        frame = tk.Frame(self.minigames_ratio)
        frame.grid(row=0, column=0, sticky="nsew", padx=10)
        for column in range(3):
            frame.columnconfigure(column, weight=1, uniform="minigames")

        title_label = tk.Label(frame, text="Minigames Ratio")
        title_label.grid(row=0, column=0, columnspan=3, padx=10)

        for i, game in enumerate(self.games.get_minigames()):
            self.load_minigame_stats(frame, game, i // 3 + 1, i % 3)

    def load_minigame_stats(self, parent: tk.Frame, minigame, row: int, column: int) -> None:
        key = minigame.NAME.lower().replace(" ", "")
        stats = self.save.data["minigames"][key]

        cell = tk.Frame(parent, borderwidth=1, relief="solid")
        cell.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)

        game_name = tk.Label(cell, text=minigame.NAME)
        game_name.grid(row=0, column=0, columnspan=2, padx=10)

        values = [stats["win"], stats["tie"], stats["lose"]]

        if sum(values) == 0:
            no_data = tk.Label(cell, text="No games played yet")
            no_data.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
            return

        cell.columnconfigure(0, weight=1)

        figure = Figure(figsize=(2, 2), layout="constrained")
        axes = figure.add_subplot()
        pie = axes.pie(values, colors=["#4caf50", "#9e9e9e", "#e53935"])

        labels = [f"{value}" if value else "" for value in values]
        axes.pie_label(pie, labels, textprops=dict(color="w", size=10, weight="bold"))

        figure.legend(pie.wedges, ["Wins", "Ties", "Loses"],
                      loc="outside lower center",
                      ncol=3,
                      fontsize=8,
                      frameon=False)

        canvas = FigureCanvasTkAgg(figure, master=cell)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Keep the chart square: its height follows the width of the column
        widget.bind("<Configure>", lambda event: widget.configure(height=event.width)
        if event.height != event.width else None, add="+")
