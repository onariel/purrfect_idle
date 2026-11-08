import tkinter as tk
from tkinter import ttk
from random import *
from Cat_counter import CatCounter

cats = CatCounter()



def launch():
    colors = ['#3f2e4f', '#77d584', '#0eb0de', '#ef38a1', '#d8c8a2']
    # Root Window
    root = tk.Tk()
    root.title("Purrfect Idle")
    root.geometry("1080x720")

    # Three columns: sides = 1 part each, center = 3 parts
    root.columnconfigure(0, weight=1, uniform="cols")
    root.columnconfigure(1, weight=3, uniform="cols")
    root.columnconfigure(2, weight=1, uniform="cols")
    root.rowconfigure(0, weight=1)

    # Left column: clicker
    clicker = tk.Frame(root, bg="#F6C6D0")  # pink
    clicker.grid(row=0, column=0, sticky="nsew")

    # Center column: tabs
    nav = ttk.Notebook(root)
    nav.grid(row=0, column=1, sticky="nsew")

    frame1 = tk.Frame(nav, bg="#FFF3C4")  # light yellow
    frame2 = tk.Frame(nav, bg="#27F5A3")
    nav.add(frame1, text="Game")
    nav.add(frame2, text="Statistics")

    # Right column: upgrades
    upgrades = tk.Frame(root, bg="#C4E3F6")  # light blue
    upgrades.grid(row=0, column=2, sticky="nsew")

    # Label inside column
    nb_of_cats = tk.Label(clicker, text=str(cats.get_cats()[0]) + "*10**" + str(cats.get_cats()[1]))
    nb_of_cats.grid(row=5, column=2, sticky="nsew")

    def updates():
        cats.update_cats(100)
        nb_of_cats.config(text=str(cats.get_cats()[0]) + "*10**" + str(cats.get_cats()[1]))
        print(cats.get_cats())
        #cats.update_cats_per_second([1,0])
        #color = colors[randint(0, 4)]
        #clicker.config(bg=color)
        clicker.after(100, updates)


    updates()

    root.mainloop()
