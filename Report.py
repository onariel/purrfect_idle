from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from Cat_counter import CatCounter
from json_mgmt import JsonMGMT
from minigames.minigames import Minigames
from graph import draw_minigame_pie

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
                pdf.savefig(self.minigames_page())
            print("Report exported successfully")
        except Exception as e:
            print(e)

    def statistics_page(self) -> Figure:
        figure = Figure(figsize=A4)
        figure.suptitle("Purrfect Idle - Statistics", fontsize=16, weight="bold")

        figure.text(0.1, 0.88, f"Total Cat Count: {self.cats.get_cats()}")
        figure.text(0.1, 0.85, f"Cat per Second: {self.cats.get_cats_per_second()}")
        figure.text(0.1, 0.82, f"Cat per Clicks: {self.cats.get_cats_per_click()}")

        rows = []
        for entity_name, entity in self.save.data["entities"].items():
            cps = f"{entity['flat_cps']}*10**{entity['flat_cps_power_of_ten']}"
            rows.append([entity_name, entity["amount_bought"], cps])

        axes = figure.add_axes((0.1, 0.3, 0.8, 0.45))
        axes.axis("off")
        axes.set_title("Entities Statistics")
        axes.table(cellText=rows,
                   colLabels=["Entities", "Quantity", "Cumulative Productions"],
                   loc="upper center")
        return figure

    def minigames_page(self) -> Figure:
        figure = Figure(figsize=A4, layout="constrained")
        figure.suptitle("Minigames Ratio", fontsize=16, weight="bold")

        games = self.games.get_minigames()
        rows = max(1, (len(games) + 2) // 3)
        for i, game in enumerate(games):
            key = game.NAME.lower().replace(" ", "")
            stats = self.save.data["minigames"][key]
            values = [stats["win"], stats["tie"], stats["lose"]]

            axes = figure.add_subplot(rows, 3, i + 1)
            axes.set_title(game.NAME)
            if sum(values) == 0:
                axes.axis("off")
                axes.text(0.5, 0.5, "No games played yet", ha="center")
                continue
            draw_minigame_pie(axes, values)

        return figure
