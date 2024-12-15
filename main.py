import tkinter as tk
from ctypes import windll

from constants import *
from power_functions import get_working_area, set_app_window
from ui.game_page import GamePage
from ui.homepage import HomePage


class SudokuApp(tk.Tk):
    # hwnd = None
    # title_bar = None
    # icon_label = None
    # title_label = None
    # # border = {}
    # resize_button = None
    # maximized = False
    # current_size = None
    # default_size = None
    # max_size = None
    # frames = {}

    def __init__(self):
        super().__init__(baseName="Sudoku")
        # self.title("Sudoku")
        self.configure(background=background)
        display_width, display_height = get_working_area()
        self.max_size = (display_width, display_height)
        self.wm_maxsize(display_width, display_height)
        top = int(display_height / 2 - min_app_height / 2)
        left = int(display_width / 2 - min_app_width / 2)
        self.current_size = self.default_size = f"{min_app_width}x{min_app_height}+{left}+{top}"
        self.geometry(self.default_size)
        self.minsize(min_app_width, min_app_height)
        self.overrideredirect(True)
        self.frames = {}
        self.maximized = False

        icon_path = "res\\rounded_icon.png"
        icon_image = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, icon_image)

        for side in ["top", "bottom", "left", "right"]:
            border = tk.Frame(self, bg="grey", relief="sunken")
            if side == "top":
                border.configure(cursor="sb_v_double_arrow")
                border.pack(side="top", fill="x", ipady=0.4)
            elif side == "bottom":
                border.configure(cursor="sb_v_double_arrow")
                border.pack(side="bottom", fill="x", ipady=0.4)
            elif side == "left":
                border.configure(cursor="sb_h_double_arrow")
                border.pack(side="left", fill="y", ipadx=0.4)
            elif side == "right":
                border.configure(cursor="sb_h_double_arrow")
                border.pack(side="right", fill="y", ipadx=0.4)
            border.bind("<B1-Motion>",
                        lambda event, current_side=side: self.resize_window(side=current_side, event=event))

        self.title_bar = tk.Frame(self, bg="grey", relief="flat")
        self.title_bar.pack(fill="x", side="top")
        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_bar.bind("<Double-Button-1>", lambda x: self.restore_to_default())

        self.icon_label = tk.Label(self.title_bar, image=icon_image, bg="grey")
        self.icon_label.image = icon_image  # Keep a reference to avoid garbage collection
        self.icon_label.pack(side="left", padx=5)
        self.icon_label.bind("<B1-Motion>", self.move_window)

        self.title_label = tk.Label(self.title_bar, text="Sudoku", bg="grey", fg="black",
                                    font=("Monotype Corsiva", 16, "bold"))
        self.title_label.pack(side="left")
        self.title_label.bind("<B1-Motion>", self.move_window)

        close_button = tk.Button(self.title_bar, text=close_icon, bg="grey", fg="white", font=("default", 16),
                                 relief="flat", activebackground="#910707", command=self.quit)
        close_button.pack(side="right")
        close_button.bind("<Enter>", lambda x: close_button.config(background="#910707", foreground="black"))
        close_button.bind("<Leave>", lambda x: close_button.config(background="grey", foreground="white"))

        self.resize_button = tk.Button(self.title_bar, text=maximize_icon, bg="grey", fg="white",
                                       activebackground="grey", font=("default", 16), relief="flat",
                                       command=lambda: self.resize_window(side="do_max"))
        self.resize_button.pack(side="right")
        self.resize_button.bind("<Enter>", lambda x: self.resize_button.config(foreground="black"))
        self.resize_button.bind("<Leave>", lambda x: self.resize_button.config(foreground="white"))

        minimize_button = tk.Button(self.title_bar, text=minimize_icon, bg="grey", fg="white", activebackground="grey",
                                    font=("default", 16), relief="flat", command=self.in_taskbar)
        minimize_button.pack(side="right")
        minimize_button.bind("<Enter>", lambda x: minimize_button.config(foreground="black"))
        minimize_button.bind("<Leave>", lambda x: minimize_button.config(foreground="white"))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.show_home_page()
        self.hwnd = windll.user32.GetParent(self.winfo_id())
        set_app_window(self.hwnd)
        self.wm_withdraw()
        self.after(10, self.wm_deiconify)

    def move_window(self, event):
        def move(event_2):  # runs when window is dragged
            # self.config(cursor="fleur")
            width_ = width
            height_ = height
            new_x = event_2.x_root - x_offset
            new_y = event_2.y_root - y_offset

            # left-overflow
            if new_x < 0:
                new_x = 0
            # top-overflow
            if new_y < 0:
                new_y = 0
            # right-overflow
            if new_x > max_width - int(width * 0.1):
                new_x = max_width - int(width * 0.1)
            # bottom-overflow
            if new_y > max_height - int(height * 0.1):
                new_y = max_height - int(height * 0.1)

            new_pos = f"{width_}x{height_}+{new_x}+{new_y}"
            self.geometry(new_pos)
            self.current_size = new_pos

        def release_window(_event=None):
            self.config(cursor="arrow")
            self.title_bar.bind("<B1-Motion>", self.move_window)
            self.title_label.bind("<B1-Motion>", self.move_window)
            self.icon_label.bind("<B1-Motion>", self.move_window)

        self.config(cursor="fleur")
        size_part, x, y = self.current_size.split("+")
        width, height = size_part.split("x")
        width, height, x, y = int(width), int(height), int(x), int(y)
        max_width, max_height = self.max_size

        mouse_x = event.x_root
        mouse_y = event.y_root

        if self.maximized:
            half_width = int(width / 2)
            x_offset = half_width
            y_offset = mouse_y
            if mouse_x < half_width:
                x_offset = mouse_x
            elif mouse_x + half_width > max_width:
                x_offset = mouse_x + (2 * half_width) - max_width
            self.resize_button.config(text=maximize_icon, command=lambda: self.resize_window(side="do_max"))
        else:
            x_offset = mouse_x - x
            y_offset = mouse_y - y

        self.title_bar.bind("<B1-Motion>", move)
        self.title_bar.bind("<ButtonRelease-1>", release_window)
        self.title_label.bind("<B1-Motion>", move)
        self.title_label.bind("<ButtonRelease-1>", release_window)
        self.icon_label.bind("<B1-Motion>", move)
        self.icon_label.bind("<ButtonRelease-1>", release_window)
        self.maximized = False

    def in_taskbar(self, _event=None):
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-closewindow
        windll.user32.CloseWindow(self.hwnd)

    def resize_window(self, side, event=None):
        if not event:
            if side == "do_max":
                self.resize_button.config(text=reduce_size_icon, command=lambda: self.resize_window(side="do_normal"))
                width, height = self.max_size
                self.geometry(f"{width}x{height}+0+0")
                self.maximized = True
            elif side == "do_normal":
                self.resize_button.config(text=maximize_icon, command=lambda: self.resize_window(side="do_max"))
                self.geometry(self.current_size)
                self.maximized = False
            return

        amount_x_moved, amount_y_moved = event.x, event.y
        current_pos = self.geometry()
        size_part, x, y = current_pos.split("+")
        width, height = size_part.split("x")
        width, height, x, y = int(width), int(height), int(x), int(y)
        if side in ["top", "bottom"]:
            new_height = height + amount_y_moved if side == "bottom" else height - amount_y_moved
            new_y = y if side == "bottom" else y + amount_y_moved
            if new_height > min_app_height:
                self.geometry(f"{width}x{new_height}+{x}+{new_y}")
                self.resize_button.config(text=maximize_icon, command=lambda: self.resize_window(side="do_max"))
                self.maximized = False

        elif side in ["left", "right"]:
            new_width = width + amount_x_moved if side == "right" else width - amount_x_moved
            new_x = x if side == "right" else x + amount_x_moved
            if new_width > min_app_width:
                self.geometry(f"{new_width}x{height}+{new_x}+{y}")
                self.resize_button.config(text=maximize_icon, command=lambda: self.resize_window(side="do_max"))
                self.maximized = False

        self.current_size = self.geometry()

    def restore_to_default(self):
        current_width, current_height = self.winfo_width(), self.winfo_height()
        if not (current_width == min_app_width and current_height == min_app_height):
            self.geometry(self.default_size)
            self.current_size = self.default_size
            self.resize_button.config(text=maximize_icon, command=lambda: self.resize_window(side="do_max"))
            self.maximized = False

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.pack_forget()

        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)

    def show_home_page(self):
        if "HomePage" not in self.frames:
            self.frames["HomePage"] = HomePage(self)
        self.frames["HomePage"].load_home()
        self.show_frame("HomePage")

    def load_game(self, mode, solver=False):
        self.frames["GamePage"] = GamePage(self, mode=mode, solver=solver)
        self.show_frame("GamePage")


if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()
