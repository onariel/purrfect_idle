import tkinter as tk
from tkinter import ttk
from Style import COLORS, FONTS


class Tooltip:
    """
    Small text box shown next to the mouse while hovering a widget
    Same usage as the old tkinter.tix Balloon: tooltip.bind_widget(widget, balloonmsg="text")
    """
    DELAY_MS: int = 400

    def __init__(self, window: tk.Tk) -> None:
        self.window = window
        self.messages = {}
        self.popup = None
        self.show_job = None

    def bind_widget(self, widget: tk.Widget, balloonmsg: str) -> None:
        # Calling it again on the same widget only changes the text
        is_new = widget not in self.messages
        self.messages[widget] = balloonmsg
        if is_new:
            widget.bind("<Enter>", lambda event: self.schedule(event.widget), add="+")
            widget.bind("<Leave>", lambda event: self.hide(), add="+")
            widget.bind("<ButtonPress>", lambda event: self.hide(), add="+")
            widget.bind("<Destroy>", lambda event: self.unbind_widget(event.widget), add="+")

    def unbind_widget(self, widget: tk.Widget) -> None:
        self.messages.pop(widget, None)
        self.hide()

    def schedule(self, widget: tk.Widget) -> None:
        self.hide()
        self.show_job = self.window.after(self.DELAY_MS, self.show, widget)

    def show(self, widget: tk.Widget) -> None:
        self.show_job = None
        if widget not in self.messages or not widget.winfo_exists():
            return
        self.popup = tk.Toplevel(self.window)
        # No title bar or borders from the window manager
        self.popup.wm_overrideredirect(True)
        self.popup.configure(background=COLORS['border'])
        label = ttk.Label(self.popup, text=self.messages[widget], font=FONTS['small'], padding=(6, 3),
                          background=COLORS['card'], justify="left")
        label.pack(padx=1, pady=1)
        x = widget.winfo_rootx()
        y = widget.winfo_rooty() + widget.winfo_height() + 4
        self.popup.wm_geometry(f"+{x}+{y}")

    def hide(self) -> None:
        if self.show_job is not None:
            self.window.after_cancel(self.show_job)
            self.show_job = None
        if self.popup is not None:
            self.popup.destroy()
            self.popup = None
