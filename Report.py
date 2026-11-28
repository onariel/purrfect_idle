from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
from Graph import *
import tkinter as tk
import tkinter.messagebox

A4 = (8.27, 11.69)


class Report:
    REPORT_PATH = Path("report.pdf")

    def __init__(self, cats: CatCounter, save: JsonMGMT) -> None:
        self.cats = cats
        self.save = save
        self.games = Minigames()

    def export(self) -> None:
        """Write one page per section in the PDF"""
        try:
            with PdfPages(self.REPORT_PATH) as pdf:
                pdf.savefig(self.statistics_page())
                pdf.savefig(self.all_time_cats_page())
                pdf.savefig(self.cats_sources_page())
                pdf.savefig(self.minigames_page())
            tk.messagebox.showinfo("Report Export.", "Report exported successfully!")
        except Exception as e:
            print(e)

    def statistics_page(self) -> Figure:
        figure = Figure(figsize=A4)
        figure.suptitle("Purrfect Idle - Statistics", fontsize=16, weight="bold")

        figure.text(0.1, 0.88, f"Current Cat Count: {self.cats.get_cats()}")
        figure.text(0.1, 0.85, f"Cat per Second: {self.cats.get_cats_per_second()}")
        figure.text(0.1, 0.82, f"Cat per Clicks: {self.cats.get_cats_per_click()}")
        figure.text(0.1, 0.79, f"All Time Cats: {self.cats.get_total_cats()}")
        figure.text(0.1, 0.76, f"Number of Nyan Cat clicked: {self.cats.get_nyancat_clicked()}")

        rows = []
        for entity_name, entity in self.save.data["entities"].items():
            cps = f"{self.cats.get_entity_cps(entity_name)}/s"
            rows.append([entity_name, entity["amount_bought"], cps])

        axes = figure.add_axes((0.1, 0.3, 0.8, 0.45))
        axes.axis("off")
        axes.set_title("Entities Statistics")
        axes.table(cellText=rows,
                   colLabels=["Entities", "Quantity", "Cats per seconds"],
                   loc="upper center")
        return figure

    def all_time_cats_page(self) -> Figure:
        figure = Figure(figsize=A4)
        figure.suptitle("All time cats", fontsize=16, weight="bold")

        timestamps, cats = load_all_time_cats(self.save)

        axes = figure.add_axes((0.15, 0.5, 0.75, 0.35))
        if len(timestamps) < 2:
            axes.axis("off")
            axes.text(0.5, 0.5, "Not enough data yet, keep playing!", ha="center")
            return figure
        draw_all_time_cats(axes, timestamps, cats)

        return figure

    def cats_sources_page(self) -> Figure:
        figure = Figure(figsize=A4)
        figure.suptitle("Cat sources", fontsize=16, weight="bold")

        sources = self.cats.cats_sources

        axes = figure.add_axes((0.2, 0.6, 0.7, 0.25))
        if sum(bucket["cats"] for bucket in sources.values()) == 0:
            axes.axis("off")
            axes.text(0.5, 0.5, "No cats earned yet, keep playing!", ha="center")
            return figure
        draw_cats_sources(axes, sources)

        return figure

    def minigames_page(self) -> Figure:
        figure = Figure(figsize=A4, layout="constrained")
        figure.suptitle("Minigames Ratio", fontsize=16, weight="bold")

        games = self.games.get_minigames()
        rows = max(1, (len(games) + 2) // 3)
        for i, game in enumerate(games):
            key = game.NAME.lower().replace(" ", "")
            stats = self.save.data["minigames"][key]
            values = [stats["win"], stats["lose"]]
            if game.HAS_TIE:
                values.append(stats["tie"])

            axes = figure.add_subplot(rows, 3, i + 1)
            axes.set_title(game.NAME)
            if sum(values) == 0:
                axes.axis("off")
                axes.text(0.5, 0.5, "No games played yet", ha="center")
                continue
            draw_minigame_pie(axes, stats, game.HAS_TIE)

        return figure
