import random
import tkinter as tk
from tkinter import ttk
from Cat_counter import CatCounter
from Json_MGMT import JsonMGMT
from Style import COLORS, FONTS, new_window


class TicTacToe:
    """This tic-tac-toe game is directly inspired from the following GitHub project: https://github.com/glsprasanthi/tkinter-mini-games/blob/main/tic_tac_toe.py"""
    NAME = 'Tic Tac Toe'
    PARENT_ENTITY = 'grandma'
    HAS_TIE = True

    WIN_REWARD_SECONDS = 60
    TIE_REWARD_SECONDS = 20
    LOSE_REWARD_SECONDS = 10
    CLICKS_PER_SECOND_REWARD = 1

    PLAYER = "X"
    COMPUTER = "O"
    PLAYER_COLOR = "#2196F3"
    COMPUTER_COLOR = "#FF5722"

    WIN_CONDITIONS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)  # Diagonals
    ]

    """
    Tic Tac Toe popup against the computer
    """

    def __init__(self, window: tk.Tk, cats: CatCounter, save: JsonMGMT) -> None:
        self.cats = cats
        self.save = save

        self.popup = new_window(window, self.NAME)
        self.popup.protocol("WM_DELETE_WINDOW", self.quit_game)

        self.content = None
        self.ai_job = None

        self.win_amount = max(0, save.data["minigames"]["tictactoe"]["win"])
        self.tie_amount = max(0, save.data["minigames"]["tictactoe"]["tie"])
        self.lose_amount = max(0, save.data["minigames"]["tictactoe"]["lose"])

        self.start_game()

    def start_game(self) -> None:
        """build the board from scratch"""
        if self.content is not None:
            self.content.destroy()

        self.board = [""] * 9
        self.player_turn = True

        self.content = ttk.Frame(self.popup, padding=20)
        self.content.pack(expand=True, fill="both")

        self.turn_label = ttk.Label(self.content, text="Your turn (X)",
                                    font=FONTS['heading'], foreground=self.PLAYER_COLOR)
        self.turn_label.pack(pady=(0, 10))

        grid_frame = tk.Frame(self.content, bg=COLORS['accent'], bd=5)
        grid_frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(grid_frame, text="", font=FONTS['board'], width=3, height=1,
                            bg=COLORS['card'], activebackground=COLORS['hover'], relief="flat",
                            command=lambda idx=i: self.player_move(idx))
            btn.grid(row=i // 3, column=i % 3, padx=4, pady=4)
            self.buttons.append(btn)

    def quit_game(self) -> None:
        if self.ai_job is not None:
            self.popup.after_cancel(self.ai_job)
        self.popup.destroy()

    """
    Game logic
    """

    def player_move(self, idx: int) -> None:
        if not self.player_turn or self.board[idx] != "":
            return

        self.apply_move(idx, self.PLAYER)
        if self.check_game_over():
            return

        self.player_turn = False
        self.turn_label.config(text="Computer's turn (O)", foreground=self.COMPUTER_COLOR)
        self.ai_job = self.popup.after(400, self.ai_move)

    def ai_move(self) -> None:
        """Wins if possible, else blocks the player, else takes the center, else plays randomly"""
        self.ai_job = None
        empty_indices = [i for i, val in enumerate(self.board) if val == ""]

        move = self.find_winning_move(self.COMPUTER, empty_indices)
        if move is None:
            move = self.find_winning_move(self.PLAYER, empty_indices)
        if move is None and 4 in empty_indices:
            move = 4
        if move is None:
            move = random.choice(empty_indices)

        self.apply_move(move, self.COMPUTER)
        if self.check_game_over():
            return

        self.player_turn = True
        self.turn_label.config(text="Your turn (X)", foreground=self.PLAYER_COLOR)

    def find_winning_move(self, symbol: str, empty_indices: list):
        for idx in empty_indices:
            self.board[idx] = symbol
            winner = self.get_winner()
            self.board[idx] = ""
            if winner == symbol:
                return idx
        return None

    def apply_move(self, idx: int, symbol: str) -> None:
        self.board[idx] = symbol
        color = self.PLAYER_COLOR if symbol == self.PLAYER else self.COMPUTER_COLOR
        self.buttons[idx].config(text=symbol, disabledforeground=color, state=tk.DISABLED)

    def get_winner(self):
        """Returns "X", "O", "Tie" or None if the game is not finished"""
        for a, b, c in self.WIN_CONDITIONS:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if "" not in self.board:
            return "Tie"
        return None

    def check_game_over(self) -> bool:
        winner = self.get_winner()

        if winner is None:
            return False

        if winner == self.PLAYER:
            self.win_amount += 1
            self.show_result("You win !", self.WIN_REWARD_SECONDS)
            self.save.update(self.save_result_info("w", self.win_amount))
        elif winner == self.COMPUTER:
            self.lose_amount += 1
            self.show_result("You lose ...", self.LOSE_REWARD_SECONDS)
            self.save.update(self.save_result_info("l", self.lose_amount))
        else:
            self.tie_amount += 1
            self.show_result("It's a tie.", self.TIE_REWARD_SECONDS)
            self.save.update(self.save_result_info("t", self.tie_amount))
        return True

    def save_result_info(self, result: str, value: int) -> dict:
        if result == "w":
            return {
                "minigames.tictactoe.win": value
            }
        if result == "t":
            return {
                "minigames.tictactoe.tie": value
            }
        if result == "l":
            return {
                "minigames.tictactoe.lose": value
            }
        return None

    """
    Result screen
    """

    @staticmethod
    def scale(amount: tuple, factor: int) -> tuple:
        """Multiplies a (mantissa, exponent) amount and keeps the mantissa under 1000"""
        mantissa, exponent = amount[0] * factor, amount[1]
        while mantissa >= 1000:
            mantissa /= 1000
            exponent += 3
        return round(mantissa, 3), exponent

    def reward(self, seconds: int) -> str:
        """Gives the player `seconds` of cats per second (or the minimum click reward if higher)
        and returns the amount as cats"""
        if seconds == 0:
            return "0"

        return self.cats.update_cats(seconds * 1000, "minigames")

    def show_result(self, message: str, seconds: int) -> None:
        cats_gained = self.reward(seconds)

        self.content.destroy()
        self.content = ttk.Frame(self.popup, padding=40)
        self.content.pack(expand=True, fill="both")

        result_label = ttk.Label(self.content, text=message, style="Title.TLabel")
        result_label.pack(pady=10)

        reward_label = ttk.Label(self.content, text=f"You earned {cats_gained} cats")
        reward_label.pack(pady=10)

        buttons_frame = ttk.Frame(self.content)
        buttons_frame.pack(pady=10)

        play_again_btn = ttk.Button(buttons_frame, text="Play again", style="Accent.TButton", command=self.start_game)
        play_again_btn.grid(row=0, column=0, padx=5)

        quit_btn = ttk.Button(buttons_frame, text="Quit", command=self.quit_game)
        quit_btn.grid(row=0, column=1, padx=5)
