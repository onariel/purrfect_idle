import random
import tkinter as tk
from tkinter import ttk
from Cat_counter import CatCounter
from Json_MGMT import JsonMGMT
from Style import COLORS, FONTS, new_window


class Minesweeper:
    PARENT_ENTITY = "cat-tree"
    NAME = 'Minesweeper'

    HARD_REWARD_SECONDS = 240
    MEDIUM_REWARD_SECONDS = 120
    EASY_REWARD_SECONDS = 60

    def __init__(self, window: tk.Tk, cats: CatCounter, save: JsonMGMT):
        root = new_window(window, self.NAME)

        self.cats = cats
        self.save = save
        self.root = root
        self.root.title("Minesweeper")
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.timer_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.timer_label.pack(pady=5)
        self.level_frame = tk.Frame(root)
        self.level_frame.pack(pady=10)

        tk.Label(self.level_frame, text="Select Level: ", font=("Helvetica", 12)).pack(side=tk.LEFT)
        for level in ["Easy", "Medium", "Hard"]:
            btn = tk.Button(self.level_frame, text=level, command=lambda lvl=level: self.start_game(lvl))
            btn.pack(side=tk.LEFT, padx=5)

    def start_game(self, level):
        self.level = level
        self.game_over = False
        self.flags = 0
        self.revealed = 0
        self.time_left = {"Easy": 120, "Medium": 180, "Hard": 300}[level]
        self.grid_size = {"Easy": 8, "Medium": 10, "Hard": 12}[level]
        self.total_mines = {"Easy": 10, "Medium": 15, "Hard": 25}[level]
        self.cells = {}

        # Clear previous grid
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.build_grid()
        self.place_mines()
        self.update_timer()

    def quit_game(self) -> None:
        self.root.destroy()

    def build_grid(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                btn = tk.Button(self.frame, text="", width=3, height=1, font=("Helvetica", 14),
                                command=lambda row=r, col=c: self.reveal_cell(row, col))
                btn.bind("<Button-3>", lambda e, row=r, col=c: self.toggle_flag(row, col))
                btn.grid(row=r, column=c)
                self.cells[(r, c)] = {
                    "btn": btn,
                    "mine": False,
                    "flagged": False,
                    "revealed": False,
                    "count": 0
                }

    def place_mines(self):
        positions = random.sample(list(self.cells.keys()), self.total_mines)
        for pos in positions:
            self.cells[pos]["mine"] = True

        # Count nearby mines
        for (r, c), cell in self.cells.items():
            count = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if (nr, nc) in self.cells and self.cells[(nr, nc)]["mine"]:
                        count += 1
            self.cells[(r, c)]["count"] = count

    def reveal_cell(self, r, c):
        if self.game_over:
            return

        cell = self.cells[(r, c)]
        if cell["flagged"] or cell["revealed"]:
            return

        btn = cell["btn"]
        cell["revealed"] = True
        self.revealed += 1

        if cell["mine"]:
            btn.config(text="💣", bg="red")
            self.end_game(False)
        else:
            count = cell["count"]
            btn.config(text=str(count) if count > 0 else "", bg="lightgray", relief=tk.SUNKEN)
            if count == 0:
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if (nr, nc) in self.cells:
                            self.reveal_cell(nr, nc)

        if self.check_win():
            self.end_game(True)

    def toggle_flag(self, r, c):
        if self.game_over:
            return

        cell = self.cells[(r, c)]
        btn = cell["btn"]

        if not cell["revealed"]:
            if not cell["flagged"]:
                btn.config(text="🚩", fg="blue")
                cell["flagged"] = True
                self.flags += 1
            else:
                btn.config(text="", fg="black")
                cell["flagged"] = False
                self.flags -= 1

    def check_win(self):
        return self.revealed == self.grid_size ** 2 - self.total_mines



    def update_timer(self):
        if self.game_over:
            return

        self.timer_label.config(text=f"⏱️ Time Left: {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.end_game(False)

    def reward(self, seconds: int) -> str:
        """Gives the player `seconds` of cats per second (or the minimum click reward if higher)
        and returns the amount as cats"""
        if seconds == 0:
            return "0"

        return self.cats.update_cats(seconds * 1000, "minigames")

    def end_game(self, win):
        self.game_over = True
        msg = "🎉 You Win!" if win else "💥 Game Over!"
        for (r, c), cell in self.cells.items():
            if cell["mine"] and not cell["revealed"]:
                cell["btn"].config(text="💣")
        if win:
            if self.level == "Easy":
                self.show_result(msg, self.EASY_REWARD_SECONDS)
            if self.level == "Medium":
                self.show_result(msg, self.MEDIUM_REWARD_SECONDS)
            if self.level == "Hard":
                self.show_result(msg, self.HARD_REWARD_SECONDS)
        else:
            self.show_result(msg,0)

    def show_result(self, message: str, seconds: int) -> None:
        cats_gained = self.reward(seconds)

        for child in self.root.winfo_children():
            child.destroy()

        self.frame.destroy()
        self.frame = ttk.Frame(self.root, padding=40)
        self.frame.pack(expand=True, fill="both")

        result_label = ttk.Label(self.frame, text=message, style="Title.TLabel")
        result_label.pack(pady=10)

        reward_label = ttk.Label(self.frame, text=f"You earned {cats_gained} cats")
        reward_label.pack(pady=10)

        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.pack(pady=10)

        quit_btn = ttk.Button(buttons_frame, text="OK", command=self.quit_game)
        quit_btn.grid(row=0, column=1, padx=5)