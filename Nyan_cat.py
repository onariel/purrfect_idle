import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Cat_counter import CatCounter
from Json_MGMT import JsonMGMT
from random import randint


class Nyancat:

    def __init__(self, cats: CatCounter, save: JsonMGMT, root: tk.Tk, spawn_cooldown: int,
                 lifetime: int = 8000) -> None:
        self.cats = cats
        self.save = save
        self.window = root

        self.spawn_cooldown = spawn_cooldown  # ms hidden before the cat (re)appears
        self.lifetime = lifetime  # ms on screen before it flies away by itself
        self.despawn_job = None

        # Built once, then only shown / hidden
        self.nyancat_image = self.get_nyancat_image()
        self.cat_frame = ttk.Frame(self.window, style="Nyan.TFrame")
        self.cat_button = ttk.Button(self.cat_frame, image=self.nyancat_image, style="Nyan.TButton",
                                     compound="image", cursor="hand2", command=self.nyan_on_click)
        self.cat_button.grid(row=0, column=0)

        # Start hidden, first appearance after the cooldown
        self.window.after(self.spawn_cooldown, self.spawn)

    def get_nyancat_image(self) -> ImageTk.PhotoImage:
        scale: float = 1.5
        source = Image.open("images/nyan.png")
        new_size = (int(source.width * scale), int(source.height * scale))
        source = source.resize(new_size, Image.Resampling.NEAREST)  # NEAREST keeps the pixel art sharp
        return ImageTk.PhotoImage(source)

    def spawn(self) -> None:
        # Make sure geometry is computed so winfo_width/height return the real window size
        self.window.update_idletasks()
        max_x = max(0, self.window.winfo_width() - self.cat_frame.winfo_reqwidth())
        max_y = max(0, self.window.winfo_height() - self.cat_frame.winfo_reqheight())

        # place() floats above the grid-managed columns without disturbing them
        self.cat_frame.place(x=randint(0, max_x), y=randint(0, max_y))
        self.cat_frame.lift()

        # Not clicked in time -> it disappears on its own
        self.despawn_job = self.window.after(self.lifetime, self.despawn)

    def despawn(self) -> None:
        if self.despawn_job is not None:
            self.window.after_cancel(self.despawn_job)
            self.despawn_job = None
        self.cat_frame.place_forget()
        # Come back later at a new random position
        self.window.after(self.spawn_cooldown, self.spawn)

    def nyan_on_click(self) -> None:
        # Reward = between 15 and 30 minutes of production (update_cats takes milliseconds)
        reward_time = randint(15 * 60 * 1000, 30 * 60 * 1000)
        self.cats.update_cats(reward_time)
        # Written to disk by the next autosave
        self.save.data["nyancat_clicked"] += 1
        self.despawn()
