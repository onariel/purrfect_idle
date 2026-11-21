# Purrfect Idle

> An idle game about collecting cats!

Purrfect Idle is a game about collecting an absurd amount of cats.  
To help you in this endeavor, you will recruit a wide variety of helpful tools and upgrades, like Cats, Cat Trees, Milk
or Ball of Wool.

- Collect cats and spend them to earn even more cats.

## Features

The game will be made using Python and TKinter. Your data (number of cats, which upgrade at which level, etc...) will be
saved on a json file. Some graphs will be generated using Matplotlib.

Data manipulation & File manipulation: Json save file edit and calling  
Graphical Interface: TKinter (graphs with Matplotlib)  
Report Generation: Live report (statistic page), graphical report and report exportation into a .pdf file.

## Installation

### Requirements

* Python 3 with Tkinter
* The Python packages listed in `requirements.txt` (Matplotlib and Pillow)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/onariel/purrfect_idle.git
   cd purrfect_idle
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   py -m venv .venv
   source .venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the game **from the project root** (the game loads its images and data using relative paths):
   ```bash
   py main.py
   ```

Your progress is saved in `data/save.json`, and exported reports are written to `report.pdf` in the project root.

## Note and info

This game is a direct inspiration of the [Cookie Clicker Game](https://cookieclicker.com/) made by *Julien "Orteil" Thiennot*.

## Ideas to enhancements

* prestige system: the player can reset the run up to 9 times (equals the 9 lives of a cat) in exchange of bonus
* achievements (just a plain display in popup and in a new "Achievements" page)