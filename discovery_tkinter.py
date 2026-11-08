import tkinter as tk
from tkinter import ttk
from random import *

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
tk.Label(upgrades, text="Upgrades").grid(row=1, column=0, sticky="nsew")
tk.Label(upgrades, text="Upgrades1").grid(row=1, column=1, sticky="nsew")
tk.Label(upgrades, text="Upgrades2").grid(row=2, column=0, sticky="nsew")
tk.Label(clicker, text="Current Croquet").grid(row=1, column=0, sticky="nsew")

def updates():
    color = colors[randint(0, 4)]
    clicker.config(bg=color)
    clicker.after(1000, updates)


updates()

root.mainloop()
