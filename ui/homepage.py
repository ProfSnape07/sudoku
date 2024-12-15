import tkinter as tk
from typing import Literal

from constants import *


class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent
        self.config(bg=background)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, bg=background)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=2)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=2)
        frame.columnconfigure(0, weight=1)

        self.button1 = tk.Button(frame, text="Play", foreground="black", background=background,
                                 activebackground=background, font=("Monotype Corsiva", 35, "bold"), relief="ridge",
                                 width=5, height=1, command=self.play)
        self.button1.grid(row=0, column=0, sticky="s")

        self.button2 = tk.Button(frame, text="Solve", foreground="black", background=background,
                                 activebackground=background, font=("Monotype Corsiva", 35, "bold"), relief="ridge",
                                 width=5, height=1, command=lambda: self.controller.load_game("easy", True))
        self.button2.grid(row=1, column=0)

        self.button3 = tk.Button(frame, text="Quit", foreground="black", background=background,
                                 activebackground=background, font=("Monotype Corsiva", 35, "bold"), relief="ridge",
                                 width=5, height=1, command=self.controller.quit)
        self.button3.grid(row=2, column=0, sticky="n")

    def play(self):
        self.focus_set()
        self.button1.configure(text="Easy", command=lambda: self.load_game("easy"), width=8, font=("Arial", 26))
        self.button2.configure(text="Medium", command=lambda: self.load_game("easy"), width=8, font=("Arial", 26))
        self.button3.configure(text="Hard", command=lambda: self.load_game("hard"), width=8, font=("Arial", 26))

    def load_game(self, mode: Literal["easy", "medium", "hard"]):
        self.focus_set()
        self.controller.load_game(mode=mode)

    def load_home(self):
        self.focus_set()
        self.button1.configure(text="Play", command=self.play, width=5, height=1, font=("Monotype Corsiva", 35, "bold"))
        self.button2.configure(text="Solve", command=lambda: self.controller.load_game("easy", True), width=5, height=1,
                               font=("Monotype Corsiva", 35, "bold"))
        self.button3.configure(text="Quit", command=self.controller.quit, width=5, height=1,
                               font=("Monotype Corsiva", 35, "bold"))
