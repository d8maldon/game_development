import tkinter as tk
import random
from tkinter import messagebox
import time

class Minesweeper:
    def __init__(self, master, rows=10, columns=10, mines=10):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.buttons = []
        self.mines_positions = set()
        self.is_game_over = False
        self.start_time = None
        self.timer_id = None

        self.setup_ui()
        self.place_mines()
        self.update_numbers()

    def setup_ui(self):
        self.master.title("Minesweeper")
        self.master.configure(bg="#f0f0f0")

        # Header frame
        self.header_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.header_frame.grid(row=0, column=0, columnspan=self.columns)

        # Mine counter
        self.mine_counter = tk.Label(self.header_frame, text=f"Mines: {self.mines}", font=('Arial', 14), bg="#f0f0f0")
        self.mine_counter.grid(row=0, column=0, padx=10)

        # Reset button
        self.reset_button = tk.Button(self.header_frame, text="😊", font=('Arial', 14), command=self.reset_game, bg="#d1e7dd", activebackground="#f8f9fa")
        self.reset_button.grid(row=0, column=1, padx=10)

        # Timer
        self.timer_label = tk.Label(self.header_frame, text="Time: 0", font=('Arial', 14), bg="#f0f0f0")
        self.timer_label.grid(row=0, column=2, padx=10)

        # Game board
        self.board_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.board_frame.grid(row=1, column=0)

        for r in range(self.rows):
            row = []
            for c in range(self.columns):
                button = tk.Button(self.board_frame, width=3, height=1, font=('Arial', 14), 
                                   bg="#d1e7dd", activebackground="#f8f9fa")
                button.bind("<Button-1>", lambda e, row=r, col=c: self.reveal_tile(row, col))
                button.bind("<Button-3>", lambda e, row=r, col=c: self.toggle_flag(row, col))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        while len(self.mines_positions) < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.columns - 1)
            self.mines_positions.add((row, col))

    def update_numbers(self):
        self.numbers = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        for (r, c) in self.mines_positions:
            for i in range(max(0, r-1), min(self.rows, r+2)):
                for j in range(max(0, c-1), min(self.columns, c+2)):
                    if (i, j) not in self.mines_positions:
                        self.numbers[i][j] += 1

    def reveal_tile(self, row, col):
        if self.is_game_over:
            return
        if not self.start_time:
            self.start_time = time.time()
            self.update_timer()
        button = self.buttons[row][col]
        if button.cget("state") == "disabled":
            return
        if (row, col) in self.mines_positions:
            self.game_over(False)
        else:
            self.reveal(row, col)
            if self.check_win():
                self.game_over(True)

    def reveal(self, row, col):
        button = self.buttons[row][col]
        button.config(state="disabled", relief=tk.SUNKEN, bg="#e9ecef", disabledforeground="#495057")
        if self.numbers[row][col] > 0:
            button.config(text=str(self.numbers[row][col]))
        else:
            for i in range(max(0, row-1), min(self.rows, row+2)):
                for j in range(max(0, col-1), min(self.columns, col+2)):
                    if self.buttons[i][j].cget("state") != "disabled":
                        self.reveal(i, j)

    def toggle_flag(self, row, col):
        button = self.buttons[row][col]
        if button.cget("state") == "disabled":
            return
        if button.cget("text") == "":
            button.config(text="F", fg="#dc3545")
        elif button.cget("text") == "F":
            button.config(text="")

    def game_over(self, won):
        self.is_game_over = True
        if won:
            self.reset_button.config(text="😎")
            messagebox.showinfo("Minesweeper", "Congratulations! You won!")
        else:
            self.reset_button.config(text="😢")
            messagebox.showerror("Minesweeper", "Game Over! You hit a mine.")
        for r, c in self.mines_positions:
            self.buttons[r][c].config(text="*", bg="#dc3545")
        if self.timer_id:
            self.master.after_cancel(self.timer_id)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.buttons[r][c].cget("state") != "disabled" and (r, c) not in self.mines_positions:
                    return False
        return True

    def update_timer(self):
        if self.is_game_over:
            return
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed_time}")
        self.timer_id = self.master.after(1000, self.update_timer)

    def reset_game(self):
        self.mines_positions = set()
        self.is_game_over = False
        self.start_time = None
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        self.mine_counter.config(text=f"Mines: {self.mines}")
        self.timer_label.config(text="Time: 0")
        self.reset_button.config(text="😊")
        for row in self.buttons:
            for button in row:
                button.config(state="normal", relief=tk.RAISED, text="", bg="#d1e7dd", activebackground="#f8f9fa")
        self.place_mines()
        self.update_numbers()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
