import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# White and off-white everywhere, with a very light lilac as the only accent
COLORS: dict = {
    'bg': '#fafafa', 'card': '#ffffff', 'accent': '#dee2ff', 'accent_dark': '#cdd3f5',
    'highlight': '#eef0ff', 'tab': '#f2f2f2', 'button': '#f5f5f5', 'border': '#e5e5e5',
    'hover': '#ececec', 'line': '#e5e7eb',
    'text': '#1f2937', 'muted': '#6b7280',
    'buyable_text_bg': '#C8EACB', 'buyable_card_bg': '#C8EACB',
    'not_buyable_text_bg': '#ff9b9b', 'not_buyable_card_bg': '#ff9b9b',
    'not_buyable_upgrade_bg': '#e5e5e5',
}

# Filled in by setup_style(), once the root window exists
FONTS: dict = {}


def pick_font(root: tk.Tk, names: list, size: int, weight: str = 'normal') -> tuple:
    """Use the first font family from names that this computer has"""
    available = tkfont.families(root)
    for name in names:
        if name in available:
            return name, size, weight
    return 'Segoe UI', size, weight


def setup_style(root: tk.Tk) -> None:
    """Colors and fonts for every ttk widget of the app"""
    ui_font = ['Segoe UI', 'SF Pro Text', 'Helvetica Neue', 'Cantarell', 'Noto Sans', 'Ubuntu', 'DejaVu Sans']
    # update() instead of reassigning, so modules that imported FONTS see the values
    FONTS.update({
        'title': pick_font(root, ui_font, 18, 'bold'),
        'heading': pick_font(root, ui_font, 13, 'bold'),
        'normal': pick_font(root, ui_font, 11),
        'bold': pick_font(root, ui_font, 11, 'bold'),
        'big_number': pick_font(root, ui_font, 22, 'bold'),
        'small': pick_font(root, ui_font, 9),
        'board': pick_font(root, ui_font, 32, 'bold'),
    })

    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('.', background=COLORS['bg'], foreground=COLORS['text'], font=FONTS['normal'],
                    bordercolor=COLORS['border'], lightcolor=COLORS['bg'], darkcolor=COLORS['bg'])

    # labels
    style.configure('Title.TLabel', font=FONTS['title'])
    style.configure('Section.TLabel', font=FONTS['heading'])
    style.configure('Muted.TLabel', foreground=COLORS['muted'], font=FONTS['small'])
    style.configure('Number.TLabel', font=FONTS['big_number'])

    # cards
    style.configure('Card.TFrame', background=COLORS['card'], relief='solid', borderwidth=1,
                    bordercolor=COLORS['border'])
    style.configure('Card.TLabel', background=COLORS['card'])
    style.configure('CardTitle.TLabel', background=COLORS['card'], font=FONTS['bold'])
    style.configure('Number.Card.TLabel', background=COLORS['card'], font=FONTS['big_number'])
    style.configure('Muted.Card.TLabel', background=COLORS['card'], foreground=COLORS['muted'])

    # upgrade cards, green when buyable and red otherwise
    style.configure('Buyable.TFrame', background=COLORS['buyable_card_bg'], relief='solid', borderwidth=1,
                    bordercolor=COLORS['border'])
    style.configure('Buyable.TLabel', background=COLORS['buyable_text_bg'])
    style.configure('NotBuyable.TFrame', background=COLORS['not_buyable_card_bg'], relief='solid',
                    borderwidth=1, bordercolor=COLORS['border'])
    style.configure('NotBuyable.TLabel', background=COLORS['not_buyable_text_bg'])

    # upgrade buttons, colored when buyable and grey (with a black and white image) otherwise
    style.configure('Buyable.TButton', background=COLORS['buyable_card_bg'], bordercolor=COLORS['border'],
                    lightcolor=COLORS['buyable_card_bg'], darkcolor=COLORS['buyable_card_bg'])
    style.map('Buyable.TButton', background=[('active', COLORS['accent'])],
              lightcolor=[('active', COLORS['accent'])], darkcolor=[('active', COLORS['accent'])])
    style.configure('NotBuyable.TButton', background=COLORS['not_buyable_upgrade_bg'], bordercolor=COLORS['border'],
                    lightcolor=COLORS['not_buyable_upgrade_bg'], darkcolor=COLORS['not_buyable_upgrade_bg'])
    style.map('NotBuyable.TButton', background=[('active', COLORS['not_buyable_upgrade_bg'])],
              lightcolor=[('active', COLORS['not_buyable_upgrade_bg'])],
              darkcolor=[('active', COLORS['not_buyable_upgrade_bg'])])

    # buttons
    style.configure('TButton', padding=(12, 6), background=COLORS['button'],
                    bordercolor=COLORS['border'], lightcolor=COLORS['button'], darkcolor=COLORS['button'])
    style.map('TButton', background=[('active', COLORS['hover'])])
    style.configure('Accent.TButton', background=COLORS['accent'], foreground=COLORS['text'], font=FONTS['bold'],
                    bordercolor=COLORS['accent'], lightcolor=COLORS['accent'], darkcolor=COLORS['accent'])
    style.map('Accent.TButton', background=[('active', COLORS['accent_dark'])],
              lightcolor=[('active', COLORS['accent_dark'])], darkcolor=[('active', COLORS['accent_dark'])])
    # image-only clicker: no border and blends into the card in every state, the pulse is the click feedback
    style.configure('Image.TButton', padding=(8, 16), relief='flat', borderwidth=0,
                    background=COLORS['card'], bordercolor=COLORS['card'], focuscolor=COLORS['card'],
                    lightcolor=COLORS['card'], darkcolor=COLORS['card'])
    # Explicit card colour so the TButton hover/pressed colours are not inherited
    style.map('Image.TButton',
              background=[('pressed', COLORS['card']), ('active', COLORS['card'])],
              bordercolor=[('pressed', COLORS['card']), ('active', COLORS['card'])],
              lightcolor=[('pressed', COLORS['card']), ('active', COLORS['card'])],
              darkcolor=[('pressed', COLORS['card']), ('active', COLORS['card'])],
              relief=[('pressed', 'flat')])

    # notebook tabs
    style.configure('TNotebook', background=COLORS['bg'], bordercolor=COLORS['line'])
    style.configure('TNotebook.Tab', background=COLORS['tab'], padding=(14, 6), bordercolor=COLORS['line'])
    style.map('TNotebook.Tab', background=[('selected', COLORS['bg']), ('active', COLORS['highlight'])])

    style.configure('TSeparator', background=COLORS['line'])
    root.configure(background=COLORS['bg'])


def new_window(parent: tk.Tk, title: str) -> tk.Toplevel:
    """A popup window that follows the app colors"""
    window = tk.Toplevel(parent)
    window.title(title)
    window.transient(parent)
    window.configure(background=COLORS['bg'])
    return window
