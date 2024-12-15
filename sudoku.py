from random import choice, randint
from typing import Literal


class Sudoku:
    def __init__(self, board=None):
        self.temp = 0
        if not board or len(board) != 9 or len(board[0]) != 9:
            self.random_board(mode="easy")
        else:
            self.board = [row[:] for row in board]
            self.solution = [row[:] for row in board]
            self.solved = False

    def __str__(self):
        return self.format_board(self.board, solution=False)

    def format_solution(self):
        if self.solved:
            return self.format_board(self.solution, solution=True)
        else:
            return "Sudoku is not solved."

    @staticmethod
    def format_board(sudoku, solution):
        if solution:
            board = "==== Solved Sudoku ====\n"
        else:
            board = "==== Sudoku 9*9 ====\n"
        for row in range(len(sudoku)):
            if row % 3 == 0 and row != 0:
                board += "-" * 22 + "\n"
            for col in range(len(sudoku[row])):
                if col % 3 == 0 and col != 0:
                    board += "| "
                board += f"{sudoku[row][col] or '_'} "
            board = board[:-1]
            board += "\n"
        return board[:-1]

    def backtracking_solver(self, row=0, col=0):
        if row == len(self.solution):
            self.solved = True
            return True
        if self.solution[row][col] == 0:
            for digit in range(1, 10):
                if self.valid_placement(self.solution, row, col, digit):
                    self.solution[row][col] = digit
                    if col == len(self.solution[0]) - 1:
                        if self.backtracking_solver(row=row + 1):
                            return True
                    else:
                        if self.backtracking_solver(row=row, col=col + 1):
                            return True
                    self.solution[row][col] = 0

        elif col == len(self.solution[0]) - 1:
            return self.backtracking_solver(row=row + 1)
        else:
            return self.backtracking_solver(row=row, col=col + 1)
        return False

    @staticmethod
    def valid_placement(board: list[list[int]], row: int, col: int, digit_to_place: int) -> bool:
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

    def checker(self, board, complete=True):
        row, col, grid = {}, {}, {}

        for i in range(9):
            for j in range(9):
                current_num = board[i][j]
                if current_num == 0 and complete:
                    return False
                if current_num == 0:
                    # skips check when checking for solver
                    continue
                if self.board[i][j] != 0 and self.board[i][j] != board[i][j]:
                    return False

                if i not in row:
                    row[i] = []
                if j not in col:
                    col[j] = []
                grid_key = f"{i // 3}{j // 3}"
                if grid_key not in grid:
                    grid[grid_key] = []

                # Check for duplicates in the row, column, or 3x3 grid
                if current_num in row[i] or current_num in col[j] or current_num in grid[grid_key]:
                    return False

                row[i].append(board[i][j])
                col[j].append(board[i][j])
                grid[grid_key].append(board[i][j])
        return True

    def random_board(self, mode: Literal["easy", "medium", "hard"] = "easy"):
        def fill_subgrid(board_, index):
            digits = list(range(1, 10))
            for row_ in range(index, index + 3):
                for col_ in range(index, index + 3):
                    random_digit = choice(digits)
                    digits.remove(random_digit)
                    board_[row_][col_] = random_digit
            return board_

        board = [[0] * 9 for _ in range(9)]
        # top-left grid
        board = fill_subgrid(board, 0)
        # center grid
        board = fill_subgrid(board, 3)
        # bottom-right grid
        board = fill_subgrid(board, 6)

        # self.set_board(board)
        self.__init__(board)
        self.backtracking_solver()
        board = [row[:] for row in self.solution]

        if mode == "hard":
            difficulty_factor, min_show, max_show = 2530, 17, 24
        elif mode == "medium":
            difficulty_factor, min_show, max_show = 3703, 25, 35
        else:
            difficulty_factor, min_show, max_show = 4929, 35, 40

        # turning_off
        total_showing = 81
        for row in range(9):
            for col in range(9):
                random_number = randint(1, 10000)
                if random_number > difficulty_factor:
                    # turn_off
                    board[row][col] = 0
                    total_showing -= 1

        new_showing = randint(min_show, max_show)

        # too many off
        if total_showing < min_show:
            while total_showing != new_showing:
                row = randint(0, 8)
                col = randint(0, 8)
                if board[row][col] == 0:
                    board[row][col] = self.solution[row][col]
                    total_showing += 1
        # too many on
        if total_showing > max_show:
            while total_showing != new_showing:
                row = randint(0, 8)
                col = randint(0, 8)
                if board[row][col] != 0:
                    board[row][col] = 0
                    total_showing -= 1

        self.board = [row[:] for row in board]


if __name__ == "__main__":
    ab = Sudoku()
    print(ab)
