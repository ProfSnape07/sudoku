import tkinter as tk
# from tkinter import messagebox
from typing import Literal

from constants import *
from sudoku import Sudoku
from time import sleep, time


class GamePage(tk.Frame):
    def __init__(self, parent, mode: Literal["easy", "medium", "hard"] = "easy", solver=False):
        super().__init__(parent)
        self.controller = parent
        self.configure(bg=background)

        self.mode = mode
        self.solver = solver
        self.entries: list[list[None | tk.Entry]] = [[None] * 9 for _ in range(9)]  # To keep track of entry widgets
        self.solve_button = None
        self.submit_button = None
        self.notes_frame = None
        self.notes_text = None
        self.alert_frame = None
        self.alert_label = None
        self.alert_close_button = None
        self.alert_message = None
        self.alert_button_frame = None
        self.option1 = None
        self.option2 = None

        # temp var, check and fit into correct one
        self.t_solved = False
        self.solvable = True
        self.t_solution: list[list[int]] = [[0] * 9 for _ in range(9)]
        # self.counter = 0
        self.start_time = 0
        self.sleep_time = 0.003

        if solver:
            board = [[0] * 9 for _ in range(9)]
            self.game = Sudoku(board)
        else:
            self.game = Sudoku()
            self.game.random_board(mode=mode)

        self.previous_board: list[list[int]] = self.game.board

        self.create_widgets()

    def create_widgets(self):
        outer_frame = tk.Frame(self, bg=background)
        outer_frame.pack()

        grid_frame = tk.Frame(outer_frame, bg=background)
        grid_frame.pack(padx=25, pady=25)
        validate = (self.register(self.validate_input), "%P")
        for row in range(9):
            for col in range(9):
                entry = tk.Entry(grid_frame, width=3, justify="center", font=("Helvetica", 18, "bold"),
                                 validate="key", validatecommand=validate, disabledforeground="black",
                                 foreground="blue", relief="flat")
                entry.grid(row=row, column=col, padx=3, pady=3)
                valid_sub_grids = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
                if (row // 3, col // 3) in valid_sub_grids:
                    entry.configure(highlightthickness=5, highlightbackground="black", highlightcolor="black")

                self.entries[row][col] = entry

        button_frame = tk.Frame(outer_frame, bg=background)
        button_frame.pack(fill="x")
        if self.solver:
            button_frame.rowconfigure(0, weight=1)
            button_frame.columnconfigure((0, 1), weight=1)
        else:
            button_frame.rowconfigure(0, weight=1)
            button_frame.columnconfigure((0, 1, 2, 3), weight=1)

        home = tk.Button(button_frame, text="Home", foreground="black", background=background,
                         activebackground=background, font=("Arial", 18), relief="ridge", width=6,
                         command=self.show_home_page)
        self.solve_button = tk.Button(button_frame, text="Solve", foreground="black", background=background,
                                      activebackground=background, font=("Arial", 18), relief="ridge", width=6,
                                      command=self.solve)
        note = tk.Button(button_frame, text="Notes", foreground="black", background=background,
                         activebackground=background, font=("Arial", 18), relief="ridge", width=6,
                         command=lambda: self.animate_notes(visible=False))
        # note = tk.Button(button_frame, text="Notes", foreground="black", background=background,
        #                  activebackground=background, font=("Arial", 18), relief="ridge", width=6,
        #                  command=lambda: self.make_alert("Alert !!!", "This is taking too much time.\nPlease wait !!!"))
        self.submit_button = tk.Button(button_frame, text="Submit", foreground="black", background=background,
                                       activebackground=background, font=("Arial", 18), relief="ridge", width=6,
                                       command=self.submit_game)
        # self.submit_button = tk.Button(button_frame, text="Submit", foreground="black", background=background,
        #                                activebackground=background, font=("Arial", 18), relief="ridge", width=6,
        #                                command=lambda: self.make_alert("Alert !!!", "This is taking too much time.\nPlease wait !!!", None, "as", None, "sss", None))
        # self.submit_button = tk.Button(button_frame, text="Submit", foreground="black", background=background,
        #                                activebackground=background, font=("Arial", 18), relief="ridge", width=6,
        #                                command=lambda: self.make_alert("Alert !!!",
        #                                                                "This is taking too much time.\nPlease wait !!!"))

        if self.solver:
            home.grid(row=0, column=0, padx=25, stick="w")
            self.submit_button.grid(row=0, column=1, padx=25, stick="e")
        else:
            home.grid(row=0, column=0)
            self.solve_button.grid(row=0, column=1)
            # complete.grid(row=0, column=2)
            note.grid(row=0, column=2)
            self.submit_button.grid(row=0, column=3)

        self.notes_frame = tk.Frame(outer_frame, bg="#878787")
        self.notes_frame.place(relx=1, rely=0.05, relwidth=0.5, relheight=0.95)

        close_button = tk.Button(self.notes_frame, text="Close", foreground="black", background=background,
                                 activebackground=background, font=("Arial", 18), relief="ridge", width=6,
                                 command=lambda: self.animate_notes(visible=True))
        close_button.pack(side="bottom", pady=10)

        notes_label = tk.LabelFrame(self.notes_frame, bg="#878787", text="Notes", font=("Arial", 18, "bold"),
                                    foreground="black")
        notes_label.pack(side="top", fill="both", expand=True, padx=5)

        scrollbar = tk.Scrollbar(notes_label)
        scrollbar.pack(side="right", fill="y")
        self.notes_text = tk.Text(notes_label, wrap="word", font=("Arial", 14), yscrollcommand=scrollbar.set, bg=background)
        self.notes_text.pack(fill="both", expand=True)
        scrollbar.configure(command=self.notes_text.yview)

        self.alert_frame = tk.Frame(self.controller, bg="#969696")
        self.alert_frame.place(relx=1, rely=1, width=300, height=105)

        alert_title_bar = tk.Frame(self.alert_frame, bg="grey", relief="flat")
        alert_title_bar.pack(fill="x", side="top")
        self.alert_label = tk.Label(alert_title_bar, bg="grey", fg="black", font=("Monotype Corsiva", 12, "bold"))
        self.alert_label.pack(padx=5, side="left")
        self.alert_close_button = tk.Button(alert_title_bar, text=close_icon, bg="grey", fg="black", font=("default", 12), relief="flat", state="disabled", disabledforeground="#910707", activebackground="#910707")
        self.alert_close_button.pack(side="right")

        self.alert_message = tk.Text(self.alert_frame, wrap="word", font=("Arial", 14), bg="#969696", relief="flat", height=1)
        self.alert_message.configure(state="disabled")
        self.alert_message.pack(padx=5, pady=5, fill="both", expand=True)

        self.alert_button_frame = tk.Frame(self.alert_frame, bg="grey", relief="flat")
        self.alert_button_frame.pack(fill="x", side="bottom")

        self.option1 = tk.Button(self.alert_button_frame, bg="grey", fg="black", activebackground="grey", font=("default", 12), relief="raised")
        self.option1.pack(side="right", padx=8, pady=4)
        self.option1.bind("<Enter>", lambda x: self.option1.configure(font=("default", 12, "bold")))
        self.option1.bind("<Leave>", lambda x: self.option1.configure(font=("default", 12)))
        self.option2 = tk.Button(self.alert_button_frame, bg="grey", fg="black", activebackground="grey", font=("default", 12), relief="raised")
        self.option2.pack(side="right", padx=8, pady=4)
        self.option2.bind("<Enter>", lambda x: self.option2.configure(font=("default", 12, "bold")))
        self.option2.bind("<Leave>", lambda x: self.option2.configure(font=("default", 12)))

        self.fill_grid()

    def fill_grid(self, solution=False, need_edit=False):
        game = self.game.board
        if solution:
            self.solvable = self.game.backtracking_solver()
            if self.solvable:
                self.submit_to_next(solver=self.solver)
        for row in range(9):
            for col in range(9):
                entry = self.entries[row][col]
                entry.configure(state="normal", disabledforeground="black", disabledbackground="#878787")
                entry.delete(0, "end")

                if game[row][col] != 0:
                    entry.insert(0, str(game[row][col]))
                    if game[row][col] == self.previous_board[row][col]:
                        # when drawing board for play.
                        entry.configure(state="disabled", disabledforeground="black", disabledbackground="#878787")
                    else:
                        # when filling solution and user partially solved original problem.
                        entry.configure(state="disabled", disabledforeground="blue", disabledbackground="white")
                    if need_edit:
                        if self.previous_board[row][col] == 0:
                            entry.configure(state="normal")
                else:
                    if solution:
                        entry.insert(0, str(self.game.solution[row][col]))
                        entry.configure(state="disabled", disabledforeground="black", disabledbackground="white")

    @staticmethod
    def validate_input(new_value):
        if new_value == "":
            return True
        if new_value.isdigit():
            return 1 <= int(new_value) <= 9
        return False

    def solve(self):
        self.focus_set()
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = self.entries[i][j]
                cell = entry.get()
                if not cell.isdigit():
                    cell = 0
                else:
                    if self.game.board[i][j] == 0:
                        entry.configure(state="disabled", disabledforeground="blue", disabledbackground="white")
                row.append(int(cell))
            board.append(row)
        if not self.game.checker(board, complete=False):
            # messagebox.showerror("Error", "Check your entries.")
            check_command = lambda: self.alert_frame.place(relx=1, rely=1)
            home_command = lambda: self.show_home_page()
            self.make_alert(False, "Error", "Check Your entries.", check_command, "Home", home_command, "Check", check_command)
            for i in range(9):
                for j in range(9):
                    entry = self.entries[i][j]
                    cell = entry.get()
                    try:
                        cell = int(cell)
                    except ValueError:
                        pass
                    if cell != self.game.board[i][j]:
                        entry.configure(state="normal", disabledforeground="black", disabledbackground="#878787")
        else:
            self.previous_board = [row[:] for row in self.game.board]
            self.t_solution = [row[:] for row in board]
            self.game = Sudoku(board)
            self.start_time = int(time())
            self.solvable = True
            self.sleep_time = 0.003
            self.solvable = self.solve_and_display()
            if self.solvable:
                self.submit_to_next(solver=self.solver)
            else:
                messagebox.showerror("Error", "No solution exists for this problem.")
                self.fill_grid(need_edit=True)
                self.game = Sudoku(self.previous_board)

    def solve_and_display(self, row=0, col=0):
        if row == len(self.t_solution):
            self.t_solved = True
            return True
        if self.t_solution[row][col] == 0:
            for digit in range(1, 10):
                if self.solvable:
                    if self.legal_placement(self.t_solution, row, col, digit):
                        self.t_solution[row][col] = digit
                        entry = self.entries[row][col]
                        entry.configure(state="normal")
                        entry.delete(0, "end")
                        entry.insert(0, str(digit))
                        entry.configure(state="disabled", disabledbackground="white")
                        entry.update_idletasks()
                        sleep(self.sleep_time)
                        current_time = int(time())
                        if (self.start_time + 8 - 8) == current_time:
                            self.sleep_time = 0.001
                        elif (self.start_time + 13 - 13) <= current_time:
                            self.make_alert(True, "Alert !!!", "This is taking too much time.\nPlease wait !!!")
                            self.fill_grid(solution=True)
                            self.alert_frame.place(relx=1, rely=1)
                            return self.solvable
                        if col == len(self.t_solution[0]) - 1:
                            if self.solve_and_display(row=row + 1):
                                return True
                        else:
                            if self.solve_and_display(row=row, col=col + 1):
                                return True
                        self.t_solution[row][col] = 0
                        entry = self.entries[row][col]
                        entry.configure(state="disabled", disabledbackground="black")
                        entry.update_idletasks()
                        sleep(self.sleep_time)
        elif col == len(self.t_solution[0]) - 1:
            return self.solve_and_display(row=row + 1)
        else:
            return self.solve_and_display(row=row, col=col + 1)
        return False

    @staticmethod
    def legal_placement(board: list[list[int]], row: int, col: int, digit_to_place: int) -> bool:
        # check row
        for row_range in range(len(board)):
            if board[row_range][col] == digit_to_place:
                return False
        # check col
        for col_range in range(len(board[0])):
            if board[row][col_range] == digit_to_place:
                return False
        # check grid
        row_starting_index = row - row % 3
        col_starting_index = col - col % 3
        for row in range(row_starting_index, row_starting_index + 3):
            for col in range(col_starting_index, col_starting_index + 3):
                if board[row][col] == digit_to_place:
                    return False
        return True

    def submit_game(self):
        if self.solver:
            self.solve()
            return
        self.focus_set()
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = self.entries[i][j].get()
                if not entry.isdigit():
                    self.make_alert(
                        False,
                        "Error",
                        "Missing entry in the solution.\nDo you want to continue playing?",
                        lambda: self.alert_frame.place(relx=1, rely=1),
                        "Home", self.show_home_page,
                        "Continue", lambda: self.alert_frame.place(relx=1, rely=1)
                    )
                    return
                row.append(int(entry))
            board.append(row)

        status = self.game.checker(board=board)
        if status:
            self.make_alert(
                False,
                "Solved!",
                "Solution is correct!\nDo you want to solve next Sudoku?",
                None,
                "Home", self.show_home_page,
                "Next Game", self.next_game
            )
        else:
            self.make_alert(
                False,
                "Error",
                "Solution is incorrect!\nDo you want to continue playing?",
                lambda: self.alert_frame.place(relx=1, rely=1),
                "Home", self.show_home_page,
                "Continue", lambda: self.alert_frame.place(relx=1, rely=1)
            )

    def submit_to_next(self, solver):
        self.focus_set()
        if solver:
            self.submit_button.configure(text="Clear", command=self.next_solver)
        else:
            self.submit_button.configure(text="Next", command=self.next_game)

    def next_solver(self):
        self.focus_set()
        board = [[0] * 9 for _ in range(9)]
        self.game = Sudoku(board)
        self.previous_board: list[list[int]] = [row[:] for row in self.game.board]
        self.fill_grid()
        self.submit_button.configure(text="Submit", command=self.submit_game)

    def next_game(self):
        self.focus_set()
        self.game.random_board(mode=self.mode)
        self.previous_board: list[list[int]] = [row[:] for row in self.game.board]
        self.fill_grid()
        self.submit_button.configure(text="Submit", command=self.submit_game)

    def animate_notes(self, visible=True):
        if visible:
            self.slide_notes(0.55, 0.0075)
            self.focus_set()
        else:
            self.slide_notes(1, -0.0075)
            self.notes_text.focus_set()

    def slide_notes(self, x, step):
        if 0.55 < x <= 1 or 0.55 <= x < 1:
            current_x = x + step
            self.notes_frame.place(relx=current_x, relwidth=0.45)
            self.after(10, self.slide_notes, current_x, step)

    def make_alert(self, animation_required:bool, title:str, message:str, *options) -> None:
        """

        :param animation_required:
        :param title:
        :param message:
        :param options: command_for_close_button, right_button, its_command, second-right_button, its_command
        :return:
        """
        alert_width, alert_height = 300, 105

        self.alert_label.configure(text=title)
        self.alert_message.configure(state="normal")
        self.alert_message.delete(1.0, "end")
        self.alert_message.insert(1.0, message)
        self.alert_message.configure(state="disabled")
        self.alert_close_button.configure(state="disabled")
        self.alert_button_frame.pack_forget()

        if options:
            if options[0]:
                self.alert_close_button.configure(state="normal", command=options[0])
                self.alert_close_button.bind("<Enter>", lambda: self.alert_close_button.configure(background="#910707", fg="white"))
                self.alert_close_button.bind("<Leave>", lambda: self.alert_close_button.configure(background="grey", fg="black"))

        if len(options) > 1:
            self.option1.configure(text=options[1], command=options[2])
            self.option2.configure(text=options[3], command=options[4])
            self.alert_button_frame.pack(fill="x", side="bottom")
            alert_height += 30


        size_part, x, y = self.controller.geometry().split("+")
        width, height = size_part.split("x")
        width, height, x, y = int(width), int(height), int(x), int(y)

        desired_x = (width/2) - (alert_width/2)
        desired_y = (height/2) - (alert_height/2)
        desired_relx = round(desired_x/width, 4)
        desired_rely = round(desired_y/height, 4)

        if animation_required:
            self.animate_alert(desired_relx, desired_rely, alert_height)
        else:
            self.alert_frame.place(relx=desired_relx, rely=desired_rely, height=alert_height)

    def animate_alert(self, relx, rely, height):
        # -0.20 -> 0.44 -> 0.36 -> 0.40
        step = 0.01

        # -0.20 -> 0.44
        current_y = round((rely * 2) - 1, 4)
        final_y = round(rely * 1.1, 4)
        self.alert_frame.place(relx=relx, rely=current_y, height=height)
        while current_y < final_y:
            current_y += step
            self.alert_frame.place(rely=current_y)
            self.update()
            sleep(0.01)

        # 0.44 -> 0.36
        current_y = round(rely * 1.1, 4)
        final_y = round(rely * 0.9, 4)
        while current_y > final_y:
            current_y -= step
            self.alert_frame.place(rely=current_y)
            self.update()
            sleep(0.01)

        # 0.36 -> 0.40
        current_y = round(rely * 0.9, 4)
        final_y = rely
        while current_y < final_y:
            current_y += step
            self.alert_frame.place(rely=current_y)
            self.update()
            sleep(0.01)
        sleep(1)

    def show_home_page(self):
        self.alert_frame.place(relx=1, rely=1)
        self.focus_set()
        self.controller.show_home_page()

    # def show_message(self, message, fail=False):
    #     if fail:
    #         user_choice = messagebox.askyesno("Error", message + "\nDo you want to continue?")
    #         if not user_choice:
    #             self.show_home_page()
    #     else:
    #         user_choice = messagebox.askyesno("Solved!", message + "\nDo you want to solve next Sudoku?")
    #         if user_choice:
    #             self.next_game()
    #         else:
    #             self.controller.show_home_page()
