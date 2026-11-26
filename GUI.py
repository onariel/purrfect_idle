import tkinter as tk
import tkinter.messagebox
from random import randint
from tkinter import ttk
from PIL import Image, ImageTk
from Cat_counter import CatCounter
from entities.Entities import Entities
from entities.Upgrades import Upgrades
from Json_MGMT import JsonMGMT
from minigames.minigames import Minigames
from Graph import Graph
from Statistics import Statistics
from convert.convert import Convert
from Report import Report
from tkinter import font as tkfont
from Style import setup_style, FONTS
from Nyan_cat import Nyancat


class GUI:
    cats: CatCounter
    window_width: int
    window_height: int
    window: tk.Tk
    clicker_column: ttk.Frame
    information_column: ttk.Notebook
    upgrade_column: ttk.Frame

    entities_frame: dict

    # 4x the 68px source image, so the pixel art stays evenly scaled at full size
    CLICKER_IMAGE_MAX_WIDTH: int = 272
    # Click pulse: the cat shrinks through these scales then goes back to full size
    CLICKER_PULSE_SCALES: tuple = (0.92, 0.86, 0.9, 0.96)
    CLICKER_PULSE_FRAME_MS: int = 30

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
        setup_style(self.window)
        self.window_width = 720
        self.window_height = 1080
        self.window.title("Purrfect Idle")
        self.window.geometry(str(self.window_height) + "x" + str(self.window_width))

        self.icon = ImageTk.PhotoImage(Image.open("images/purrfect_idle.ico"))
        self.window.iconphoto(True, self.icon)

        # Three columns: sides = 1 part each, center = 3 parts
        self.window.columnconfigure(0, weight=1, uniform="cols")
        self.window.columnconfigure(1, weight=3, uniform="cols")
        self.window.columnconfigure(2, weight=1, uniform="cols")
        self.window.rowconfigure(0, weight=1)

        self.clicker_column = ttk.Frame(self.window, style="Card.TFrame", padding=10)
        self.clicker_column.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)

        self.information_column = ttk.Notebook(self.window)
        self.information_column.grid(row=0, column=1, sticky="nsew", padx=5, pady=10)

        self.entities_bought = ttk.Frame(self.information_column)
        self.statistics = ttk.Frame(self.information_column)

        # Right column: upgrades
        self.upgrade_column = ttk.Frame(self.window)
        self.upgrade_column.grid(row=0, column=2, sticky="nsew", padx=(5, 10), pady=10)

        # Resized to the column width in resize_clicker_image()
        self.cat_image_source = Image.open("images/clicker_image.png")
        self.cat_image = ImageTk.PhotoImage(self.cat_image_source)
        self.cat_image_width = 0
        self.cat_pulse_frames = []
        self.cat_pulse_job = None

        self.init_upgrade_column()
        self.init_main_column()
        self.init_clicker_column()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.autosave()

        Nyancat(self.cats, self.save, self.window, randint(40000, 80000))

        self.window.mainloop()

    def save_file(self) -> None:
        new_save = self.cats.save_cats_info()
        self.save.update(new_save)

    def autosave(self) -> None:
        """Autosave every minutes"""
        self.save_file()
        self.window.after(10000, self.autosave)
        self.save.add_all_time_cats(self.cats.total_cats, self.cats.total_cats_power_of_ten)

    def on_close(self) -> None:
        self.save_file()
        self.window.destroy()

    """
    Clicker Column
    """

    def init_clicker_column(self) -> None:
        # Stats pinned at the top, the button centered in the remaining space
        self.clicker_column.columnconfigure(0, weight=1)
        self.clicker_column.rowconfigure(3, weight=1)

        label_cat = ttk.Label(self.clicker_column, style="Number.Card.TLabel")
        label_cat.grid(row=0, column=0, pady=(10, 0))

        label_cat_seconds = ttk.Label(self.clicker_column, style="Muted.Card.TLabel")
        label_cat_seconds.grid(row=1, column=0, pady=(0, 10))

        separator = ttk.Separator(self.clicker_column, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew")

        self.button_clicker = ttk.Button(self.clicker_column, image=self.cat_image, style="Image.TButton",
                                         command=self.on_button_clicker_column)
        self.button_clicker.grid(row=3, column=0, sticky="ew", padx=5)
        self.clicker_column.bind("<Configure>", lambda event: self.resize_clicker_image(event.width))

        self.update_clicker_column(label_cat, label_cat_seconds)

    def render_cat_image(self, width: int) -> ImageTk.PhotoImage:
        source_width, source_height = self.cat_image_source.size
        height = round(source_height * width / source_width)
        # NEAREST keeps the pixel art sharp
        return ImageTk.PhotoImage(self.cat_image_source.resize((width, height), Image.NEAREST))

    def resize_clicker_image(self, column_width: int) -> None:
        # Column padding (10) + button padx (5) + Image.TButton padding (8) on both sides
        width = min(column_width - 2 * (10 + 5 + 8), self.CLICKER_IMAGE_MAX_WIDTH)
        if width <= 0 or width == self.cat_image_width:
            return
        self.cat_image_width = width
        self.cat_image = self.render_cat_image(width)
        # Pulse frames are rendered once per size, not on every click
        self.cat_pulse_frames = [self.render_cat_image(round(width * scale)) for scale in self.CLICKER_PULSE_SCALES]
        self.button_clicker.config(image=self.cat_image)

    def pulse_clicker_image(self, frame: int = 0) -> None:
        if frame < len(self.cat_pulse_frames):
            self.button_clicker.config(image=self.cat_pulse_frames[frame])
            self.cat_pulse_job = self.window.after(self.CLICKER_PULSE_FRAME_MS, self.pulse_clicker_image, frame + 1)
        else:
            self.button_clicker.config(image=self.cat_image)
            self.cat_pulse_job = None

    def update_clicker_column(self, label_cat: ttk.Label, label_cat_seconds: ttk.Label) -> None:
        self.cats.update_cats(50)  # 50 ms
        nb_cats = self.cats.get_cats()
        nb_cats_per_seconds = self.cats.get_cats_per_second()
        label_cat.config(text=str(nb_cats) + " cats")
        label_cat_seconds.config(text=str(nb_cats_per_seconds) + " cats per seconds")
        label_cat.after(50, self.update_clicker_column, label_cat, label_cat_seconds)

    def on_button_clicker_column(self):
        self.cats.click()
        # Restart the pulse when clicking again before the previous one is over
        if self.cat_pulse_job is not None:
            self.window.after_cancel(self.cat_pulse_job)
        self.pulse_clicker_image()

    """
    Main Column
    """

    def init_main_column(self) -> None:
        self.information_column.add(self.entities_bought, text="Game")
        self.information_column.add(self.statistics, text="Statistics")

        self.init_stats_section()
        self.minigames.init_game_section(self.entities_bought, self.window, self.cats, self.save)

    def init_stats_section(self) -> None:
        self.statistics.columnconfigure(0, weight=1)

        frame = ttk.Frame(self.statistics)
        frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)

        title_label = ttk.Label(frame, text="You can view here the statistics of your game.")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        graph_btn = ttk.Button(frame, text="Open Graphical Statistics", command=lambda: self.graph_cats())
        graph_btn.grid(row=1, column=0, sticky="w", pady=10)

        save_btn = ttk.Button(frame, text="Manual Save", style="Accent.TButton", command=lambda: self.manual_save())
        save_btn.grid(row=2, column=1, pady=10, sticky="e")

        export_btn = ttk.Button(frame, text="Export", style="Accent.TButton", command=lambda: self.export_stats())
        export_btn.grid(row=1, column=1, pady=10, sticky="e")

        separator = ttk.Separator(frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        Statistics(frame, self.save, self.cats, 3)

    def export_stats(self) -> None:
        self.report.export()

    def manual_save(self) -> None:
        tk.messagebox.showinfo("Manual Save", "Successfully saved your game.")
        self.save_file()

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

    def on_entity_bought(self, event, entity_name: str) -> None:
        if self.entities_frame[entity_name]["is_buyable"]:
            self.cats.add_entity(entity_name)

    def init_upgrade_column(self) -> None:
        # One full-width row per entity, stacked from the top of the column
        self.upgrade_column.columnconfigure(0, weight=1)
        row = 0  # 3 rows are reserved for the upgrades and the title upgrade

        # Upgrades
        self.number_of_rows_of_upgrades = 2
        self.number_of_upgrades_per_row = 4
        self.upgrades: list = Upgrades.get_upgrades(self.save)
        upgrades_title_label = ttk.Label(self.upgrade_column, text="Upgrades:")
        upgrades_title_label.grid(row=row, column=0, pady=10, sticky="ew")
        row += 1

        self.calculate_which_upgrades_to_show()
        self.upgrades_frame = []
        self.upgrades_images = {}
        for i in range(self.number_of_rows_of_upgrades):
            frame = ttk.Frame(self.upgrade_column, padding=2)
            frame.grid(row=row, column=0, sticky="ew", pady=(0, 5))
            row += 1
            self.upgrades_frame.append(frame)
        self.upgrades_buttons = []

        # Entities
        entities_title_label = ttk.Label(self.upgrade_column, text="Entities")
        entities_title_label.grid(row=row, column=0, pady=10, sticky="ew")
        entities = Entities.get_entities()
        self.entities_frame = {}
        line_height = tkfont.Font(font=FONTS["normal"]).metrics("linespace")
        entity_image_size = 2 * (line_height + 2 * 5) - 2 * 5  # 2 times (text line + 5 pady) - image pady
        for entity_name in entities:
            row += 1
            self.entities_frame[entity_name] = {}
            frame = ttk.Frame(self.upgrade_column, style="NotBuyable.TFrame", padding=2)
            frame.grid(row=row + 1, column=0, sticky="ew", pady=(0, 5))
            frame.columnconfigure(1, weight=1)
            frame.bind("<Button-1>",
                       lambda event="oui", entity_name=entity_name: self.on_entity_bought(event=event,
                                                                                          entity_name=entity_name))
            self.entities_frame[entity_name]["frame"] = frame

            image_entity = ImageTk.PhotoImage(
                Image.open(f"{entities[entity_name]["image_path"]}.png").resize(
                    (entity_image_size, entity_image_size), Image.NEAREST))
            self.entities_frame[entity_name]["image"] = image_entity
            image_label = ttk.Label(frame, image=image_entity, style="NotBuyable.TLabel")
            image_label.bind("<Button-1>",
                             lambda event="oui", entity_name=entity_name: self.on_entity_bought(
                                 event=event, entity_name=entity_name))
            image_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=5, pady=5)
            self.entities_frame[entity_name]["image_label"] = image_label

            name_entity = entities[entity_name]["name"]
            label_entity_name = ttk.Label(frame,
                                          text=name_entity[:15] + "..." if len(name_entity) > 15 else name_entity,
                                          anchor="w", style="NotBuyable.TLabel")
            label_entity_name.grid(row=0, column=1, sticky="w", padx=5, pady=5)
            label_entity_name.bind("<Button-1>",
                                   lambda event="oui", entity_name=entity_name: self.on_entity_bought(
                                       event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["name"] = label_entity_name

            label_entity_quantity = ttk.Label(frame, text="quantity", anchor="w", style="NotBuyable.TLabel")
            label_entity_quantity.grid(row=1, column=1, sticky="w", padx=5, pady=5)
            label_entity_quantity.bind("<Button-1>",
                                       lambda event="oui", entity_name=entity_name: self.on_entity_bought(
                                           event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["quantity"] = label_entity_quantity

            label_entity_price = ttk.Label(frame, text=str(entities[entity_name]["price"]) + " cats", anchor="w",
                                           style="NotBuyable.TLabel")
            # Right edge of the frame, vertically centered on the two text rows
            label_entity_price.grid(row=0, column=2, rowspan=2, sticky="e", padx=5, pady=5)
            label_entity_price.bind("<Button-1>",
                                    lambda event="oui", entity_name=entity_name: self.on_entity_bought(
                                        event=event, entity_name=entity_name))
            self.entities_frame[entity_name]["price"] = label_entity_price
        self.update_upgrade_column()

    def update_upgrade_column(self) -> None:

        # upgrade update
        i = 0
        nb_of_upgrades_to_show = len(self.upgrades_to_show)
        nb_of_buttons = len(self.upgrades_buttons)
        while i < nb_of_upgrades_to_show and i < nb_of_buttons:
            button = self.upgrades_buttons[i]
            upgrade = self.upgrades_to_show[i]
            if upgrade["name"] not in self.upgrades_images:
                image = ImageTk.PhotoImage(Image.open(f"{upgrade['image_path']}"))
                self.upgrades_images[upgrade["name"]] = image
                # Black and white version, shown while the upgrade cannot be bought
                self.upgrades_images[upgrade["name"] + "NotBuyable"] = ImageTk.PhotoImage(
                    Image.open(f"{upgrade['image_path']}").convert("RGBA").convert("LA").convert("RGBA"))
            else:
                image = self.upgrades_images[upgrade["name"]]
            is_buyable = "Buyable" if self.cats.is_upgrade_buyable(upgrade) else "NotBuyable"
            if is_buyable == "NotBuyable":
                image = self.upgrades_images[upgrade["name"] + "NotBuyable"]
            if button.cget("text") != upgrade["name"]:
                button.config(padding=2,
                              text=f"{upgrade["name"]}",
                              command=lambda event="oui", upgrade=upgrade: self.on_upgrade_bought(
                                  event, upgrade), image=image, compound="image")
            button.config(image=image, style=is_buyable + ".TButton")
            i += 1

        if nb_of_upgrades_to_show > nb_of_buttons:
            while i < nb_of_upgrades_to_show:
                upgrade = self.upgrades_to_show[i]
                is_buyable = "Buyable" if self.cats.is_upgrade_buyable(upgrade) else "NotBuyable"
                if upgrade["name"] not in self.upgrades_images:
                    image = ImageTk.PhotoImage(Image.open(f"{upgrade['image_path']}"))
                    self.upgrades_images[upgrade["name"]] = image
                    # Black and white version, shown while the upgrade cannot be bought
                    self.upgrades_images[upgrade["name"] + "NotBuyable"] = ImageTk.PhotoImage(
                        Image.open(f"{upgrade['image_path']}").convert("RGBA").convert("LA").convert("RGBA"))
                else:
                    image = self.upgrades_images[upgrade["name"]]
                if is_buyable == "NotBuyable":
                    image = self.upgrades_images[upgrade["name"] + "NotBuyable"]
                button = ttk.Button(self.upgrades_frame[(i // self.number_of_upgrades_per_row)], padding=2,
                                    text=f"{upgrade["name"]}", style=is_buyable + ".TButton",
                                    command=lambda event="oui", upgrade=upgrade,: self.on_upgrade_bought(
                                        event, upgrade), image=image, compound="image")
                button.grid(row=0, column=i % self.number_of_upgrades_per_row, sticky="ew", padx=5, pady=5)
                self.upgrades_buttons.append(button)
                i += 1

        if nb_of_upgrades_to_show < nb_of_buttons:
            while i < nb_of_buttons:
                self.upgrades_buttons[i].destroy()
                self.upgrades_buttons.pop(i)
                nb_of_buttons -= 1

        # entity update
        entities = Entities.get_entities()
        for entity_key in entities:
            entity = self.cats.get_entity_info(entity_key)
            quantity_label: ttk.Label = self.entities_frame[entity_key]["quantity"]
            quantity_label.config(text=entity["amount_bought"])

            price_label: ttk.Label = self.entities_frame[entity_key]["price"]
            price_label.config(text=str(Convert.convert(entity["price"], entity["price_power_of_ten"]) + " cats"))

            name_label: ttk.Label = self.entities_frame[entity_key]["name"]

            image_label: ttk.Label = self.entities_frame[entity_key]["image_label"]

            frame: ttk.Frame = self.entities_frame[entity_key]["frame"]
            is_buyable = self.cats.is_entity_buyable(entity_key)
            prefix = "Buyable" if is_buyable else "NotBuyable"
            frame.config(style=prefix + ".TFrame")
            quantity_label.config(style=prefix + ".TLabel")
            price_label.config(style=prefix + ".TLabel")
            name_label.config(style=prefix + ".TLabel")
            image_label.config(style=prefix + ".TLabel")
            self.entities_frame[entity_key]["is_buyable"] = is_buyable

        quantity_label.after(100, self.update_upgrade_column)

    def on_upgrade_bought(self, event, upgrade: dict) -> None:
        if self.cats.is_upgrade_buyable(upgrade):
            self.upgrades.remove(upgrade)
            self.upgrades_to_show.remove(upgrade)
            self.calculate_which_upgrades_to_show()
            self.cats.buy_upgrade(upgrade)

    def calculate_which_upgrades_to_show(self) -> None:
        self.upgrades_to_show = []
        if len(self.upgrades) > self.number_of_rows_of_upgrades * self.number_of_upgrades_per_row:
            self.upgrades_to_show = self.upgrades[
                :self.number_of_rows_of_upgrades * self.number_of_upgrades_per_row].copy()
        else:
            self.upgrades_to_show = self.upgrades.copy()
