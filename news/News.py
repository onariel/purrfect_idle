import json
import tkinter as tk
from random import choice
from tkinter import ttk
from tkinter import font as tkfont
from Style import COLORS, FONTS


class News:
    """
    News ticker shown above the main column: a random news scrolls from right to left,
    and a new one starts when the previous one has fully left the screen
    """
    parent: tk.Frame
    frame: ttk.Frame
    canvas: tk.Canvas
    news_list: list

    SCROLL_STEP_PX: int = 1
    SCROLL_FRAME_MS: int = 20

    def __init__(self, parent: tk.Frame, row: int) -> None:
        self.parent = parent
        self.row = row
        self.news_list = News.get_news()

        self.current_news = ""
        self.canvas_width = 0

        self.init_news_section()

    @staticmethod
    def get_news() -> list:
        return json.load(open('news/News.json'))

    def init_news_section(self) -> None:
        self.frame = ttk.Frame(self.parent, style="Card.TFrame", padding=8)
        self.frame.grid(row=self.row, column=0, sticky="ew", pady=(0, 5))
        self.frame.columnconfigure(0, weight=1)

        # tk.Canvas is not a ttk widget, it ignores the styles so the colors are given directly
        line_height = tkfont.Font(font=FONTS["normal"]).metrics("linespace")
        self.canvas = tk.Canvas(self.frame, height=line_height, background=COLORS["card"],
                                highlightthickness=0, borderwidth=0)
        self.canvas.grid(row=0, column=0, sticky="ew")
        self.news_text = self.canvas.create_text(0, line_height // 2, anchor="w", font=FONTS["normal"],
                                                 fill=COLORS["text"])

        self.canvas.bind("<Configure>", lambda event: self.on_canvas_resize(event.width))

    def on_canvas_resize(self, canvas_width: int) -> None:
        # The real width is only known once the canvas is displayed, the ticker starts at that moment
        is_first_resize = self.canvas_width == 0
        self.canvas_width = canvas_width
        if is_first_resize:
            self.show_random_news()
            self.update_news()

    def show_random_news(self) -> None:
        # Avoid showing the same news twice in a row
        candidates = [news for news in self.news_list if news != self.current_news] or self.news_list
        self.current_news = choice(candidates)
        self.canvas.itemconfig(self.news_text, text=self.current_news)
        # Start just past the right edge
        _, y = self.canvas.coords(self.news_text)
        self.canvas.coords(self.news_text, self.canvas_width, y)

    def update_news(self) -> None:
        """Move the news to the left, every 30 ms"""
        self.canvas.move(self.news_text, -self.SCROLL_STEP_PX, 0)
        # bbox = (x1, y1, x2, y2), the news is gone once its right edge is past the left side
        if self.canvas.bbox(self.news_text)[2] < 0:
            self.show_random_news()
        self.parent.after(self.SCROLL_FRAME_MS, self.update_news)
