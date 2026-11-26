from Cat_counter import CatCounter
import tkinter as tk
from tkinter import ttk
from Json_MGMT import JsonMGMT
from minigames.minigames import Minigames
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Style import COLORS, new_window
from convert.convert import Convert
import datetime as dt

SOURCE_LABELS = {"click": "Clicks", "idle": "Idle", "nyancat": "Nyan Cat", "minigames": "Minigames"}
SOURCE_COLORS = ["#5c6bc0", "#26a69a", "#ec407a", "#ffa726"]


def draw_minigame_pie(axes, values: list) -> None:
    """Draw the win/tie/lose pie and its legend on the given axes (shared with Report)"""
    pie = axes.pie(values, colors=["#4caf50", "#9e9e9e", "#e53935"])

    labels = [f"{value}" if value else "" for value in values]
    axes.pie_label(pie, labels, textprops=dict(color="w", size=10, weight="bold"))

    # Legend attached to the axes (not the figure) so each pie keeps its own legend
    axes.legend(pie.wedges, ["Wins", "Ties", "Loses"],
                loc="upper center",
                bbox_to_anchor=(0.5, 0),
                ncol=3,
                fontsize=8,
                handlelength=1,
                columnspacing=0.8,
                frameon=False)


def load_all_time_cats(save: JsonMGMT) -> tuple[list, list]:
    """Turn the saved history into two lists that matplotlib can plot (shared with Report)"""
    timestamps = []
    cats = []
    for entry in save.data["all_time_cats"]:
        timestamps.append(dt.datetime.strptime(entry["timestamp"], JsonMGMT.TIMESTAMP_FORMAT))
        cats.append(entry["cats"] * 10 ** entry["power_of_ten"])
    return timestamps, cats


def draw_all_time_cats(axes, timestamps: list, cats: list) -> None:
    """Draw the All-time cats line on the given axes (shared with Report)"""
    axes.plot(timestamps, cats, color="#5c6bc0", linewidth=2)
    axes.set_yscale("log")  # idle numbers grow exponentially
    axes.set_ylabel("Cats")
    axes.grid(True, color=COLORS['line'])
    # Tilt the dates on these axes only so they don't overlap
    axes.tick_params(axis="x", labelrotation=30)
    for label in axes.get_xticklabels():
        label.set_horizontalalignment("right")


def draw_cats_sources(axes, sources: dict) -> None:
    """Draw the share of cats earned per source on the given axes (shared with Report)"""
    names = [SOURCE_LABELS[key] for key in sources]
    values = [bucket["cats"] * 10 ** bucket["power_of_ten"] for bucket in sources.values()]
    total = sum(values)
    shares = [value / total * 100 for value in values]

    # Horizontal bars instead of a pie: idle usually dwarfs the rest, small slices would be invisible
    bars = axes.barh(names, shares, color=SOURCE_COLORS[:len(names)])
    axes.invert_yaxis()  # first source on top
    # Extra room on the right so the label of a bar close to 100% stays visible
    axes.set_xlim(0, 135)
    axes.set_xticks(range(0, 101, 20))
    axes.set_xlabel("% of all cats earned")
    axes.grid(True, axis="x", color=COLORS['line'])
    axes.set_axisbelow(True)

    # "12.3% (4.5 Million)" next to each bar
    labels = [f"{share:.1f}% ({Convert.convert(bucket['cats'], bucket['power_of_ten']).strip()})"
              for share, bucket in zip(shares, sources.values())]
    axes.bar_label(bars, labels, padding=4, fontsize=9)


class Graph:

    def __init__(self, window: tk.Tk, cats: CatCounter, save: JsonMGMT) -> None:
        self.cats = cats
        self.save = save
        self.games = Minigames()

        self.popup = new_window(window, "Graphs")
        self.popup.geometry("800x800")

        self.popup.columnconfigure(0, weight=1, uniform="cols")
        self.popup.rowconfigure(0, weight=1)

        self.page = ttk.Notebook(self.popup)
        self.page.grid(row=0, column=0, sticky="nsew")

        self.minigames_ratio = ttk.Frame(self.page)
        self.all_time_cats = ttk.Frame(self.page)
        self.cat_sources = ttk.Frame(self.page)

        self.init_notebook()

    def init_notebook(self) -> None:
        self.page.add(self.all_time_cats, text="All time cats")
        self.page.add(self.cat_sources, text="Cat sources")
        self.page.add(self.minigames_ratio, text="Minigames Ratio")

        self.init_minigames_ratio()
        self.init_all_time_cats()
        self.init_cat_sources()

    def init_all_time_cats(self) -> None:
        self.all_time_cats.columnconfigure(0, weight=1)
        self.all_time_cats.rowconfigure(1, weight=1)

        title_frame = ttk.Frame(self.all_time_cats)
        title_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        title_label = ttk.Label(title_frame, text="All time cats", style="Title.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        subtitle_label = ttk.Label(title_frame, text="The total number of cats you gained.", style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        timestamps, cats = load_all_time_cats(self.save)

        if len(timestamps) < 2:
            no_data = ttk.Label(self.all_time_cats, text="Not enough data yet, keep playing!", style="Muted.TLabel")
            no_data.grid(row=1, column=0, padx=10, pady=10)
            return

        figure = Figure(figsize=(6, 4), layout="constrained", facecolor=COLORS['card'])
        axes = figure.add_subplot()
        draw_all_time_cats(axes, timestamps, cats)

        canvas = FigureCanvasTkAgg(figure, master=self.all_time_cats)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def init_minigames_ratio(self) -> None:
        self.minigames_ratio.columnconfigure(0, weight=1)

        title_label = ttk.Label(self.minigames_ratio, text="Minigames Ratio", style="Title.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10)

        subtitle_label = ttk.Label(self.minigames_ratio, text="The ratio of WIN / LOSS / TIE in the different games.",
                                   style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, padx=10, pady=0)

        frame = ttk.Frame(self.minigames_ratio)
        frame.grid(row=2, column=0, sticky="nsew", padx=10)
        for column in range(3):
            frame.columnconfigure(column, weight=1, uniform="minigames")

        for i, game in enumerate(self.games.get_minigames()):
            self.load_minigame_stats(frame, game, i // 3 + 1, i % 3)

    def load_minigame_stats(self, parent: tk.Frame, minigame, row: int, column: int) -> None:
        key = minigame.NAME.lower().replace(" ", "")
        stats = self.save.data["minigames"][key]

        cell = ttk.Frame(parent, style="Card.TFrame", padding=5)
        cell.grid(row=row, column=column, sticky="nsew", padx=10, pady=10)

        game_name = ttk.Label(cell, text=minigame.NAME, style="CardTitle.TLabel")
        game_name.grid(row=0, column=0, columnspan=2, padx=10)

        values = [stats["win"], stats["tie"], stats["lose"]]

        if sum(values) == 0:
            no_data = ttk.Label(cell, text="No games played yet", style="Muted.Card.TLabel")
            no_data.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
            return

        cell.columnconfigure(0, weight=1)

        figure = Figure(figsize=(2, 2), layout="constrained", facecolor=COLORS['card'])
        axes = figure.add_subplot()
        draw_minigame_pie(axes, values)

        canvas = FigureCanvasTkAgg(figure, master=cell)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(background=COLORS['card'], highlightthickness=0)
        widget.grid(row=1, column=0, columnspan=2, sticky="ew")

        # Keep the chart square: its height follows the width of the column
        widget.bind("<Configure>", lambda event: widget.configure(height=event.width)
        if event.height != event.width else None, add="+")

    def init_cat_sources(self) -> None:
        self.cat_sources.columnconfigure(0, weight=1)
        self.cat_sources.rowconfigure(1, weight=1)

        title_frame = ttk.Frame(self.cat_sources)
        title_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        title_label = ttk.Label(title_frame, text="Cat sources", style="Title.TLabel")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        subtitle_label = ttk.Label(title_frame, text="Where your cats come from.", style="Subtitle.TLabel")
        subtitle_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Read the live counter: the save only gets these values on the next autosave
        sources = self.cats.cats_sources

        if sum(bucket["cats"] for bucket in sources.values()) == 0:
            no_data = ttk.Label(self.cat_sources, text="No cats earned yet, keep playing!", style="Muted.TLabel")
            no_data.grid(row=1, column=0, padx=10, pady=10)
            return

        figure = Figure(figsize=(6, 3), layout="constrained", facecolor=COLORS['card'])
        axes = figure.add_subplot()
        draw_cats_sources(axes, sources)

        canvas = FigureCanvasTkAgg(figure, master=self.cat_sources)
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
