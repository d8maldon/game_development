import matplotlib.pyplot as plt
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), " ")
        self.current_player = "X"
        self.fig, self.ax = plt.subplots()

    def draw_board(self):
        self.ax.clear()
        for i in range(1, 3):
            self.ax.axhline(i - 0.5, color='black', linewidth=2)
            self.ax.axvline(i - 0.5, color='black', linewidth=2)
        for i in range(3):
            for j in range(3):
                if self.board[i, j] != " ":
                    self.ax.text(j, i, self.board[i, j], ha='center', va='center', fontsize=40)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(-0.5, 2.5)
        self.ax.set_ylim(2.5, -0.5)
        plt.draw()

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != " ":
                return row[0]
        for col in range(3):
            if self.board[0, col] == self.board[1, col] == self.board[2, col] != " ":
                return self.board[0, col]
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != " ":
            return self.board[0, 0]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != " ":
            return self.board[0, 2]
        return None

    def is_full(self):
        return not np.any(self.board == " ")

    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        col, row = int(event.xdata + 0.5), int(event.ydata + 0.5)
        if col < 0 or col > 2 or row < 0 or row > 2:
            return
        if self.board[row, col] != " ":
            return

        self.board[row, col] = self.current_player
        self.draw_board()
        winner = self.check_winner()
        if winner:
            plt.title(f"Player {winner} wins!")
            self.fig.canvas.mpl_disconnect(self.cid)
        elif self.is_full():
            plt.title("It's a tie!")
            self.fig.canvas.mpl_disconnect(self.cid)
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            plt.title(f"Player {self.current_player}'s turn")

    def play_game(self):
        self.fig.canvas.mpl_disconnect(self.fig.canvas.manager.key_press_handler_id)
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.title(f"Player {self.current_player}'s turn")
        self.draw_board()
        plt.show()

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
