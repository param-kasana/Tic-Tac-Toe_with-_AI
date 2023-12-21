import tkinter as tk
from tkinter import messagebox
from functools import partial

class TicTacToeGUI:
    def __init__(self):
        self.mode_selection_window = tk.Tk()
        self.mode_selection_window.title("Select Game Mode")

        tk.Label(self.mode_selection_window, text="Select Game Mode", font=('Arial', 18)).pack(pady=10)

        tk.Button(self.mode_selection_window, text="1v1 Match", font=('Arial', 14),
                  command=lambda: self.start_game(False)).pack(pady=10)

        tk.Button(self.mode_selection_window, text="vs Computer", font=('Arial', 14),
                  command=lambda: self.start_game(True)).pack(pady=10)

    def start_game(self, vs_computer):
        self.mode_selection_window.destroy()

        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")

        self.vs_computer = vs_computer
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        # Heading
        tk.Label(self.root, text="Tic-Tac-Toe", font=('Arial', 24)).grid(row=0, column=0, columnspan=3, pady=10)

        # Display Player's Turn
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=('Arial', 14))
        self.turn_label.grid(row=1, column=0, columnspan=3, pady=10)

        # Board Buttons
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text='', font=('Arial', 16), width=6, height=2,
                                   command=partial(self.on_button_click, i, j))
                button.grid(row=i + 2, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

        # Reset Game Button
        tk.Button(self.root, text="Reset Game", font=('Arial', 12), command=self.reset_game).grid(row=5, column=0, columnspan=3, pady=10)

        if self.vs_computer and self.current_player == 'O':
            self.make_computer_move()

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col]['text'] = self.current_player
            if self.check_winner():
                self.show_winner()
            elif self.is_board_full():
                self.show_draw()
            else:
                self.switch_player()
                if self.vs_computer and self.current_player == 'O':
                    self.make_computer_move()

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != ' ':
                return True
        for column in range(3):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != ' ':
            return True
        return False

    def is_board_full(self):
        return all(element != ' ' for row in self.board for element in row)

    def show_winner(self):
        messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        self.reset_game()

    def show_draw(self):
        messagebox.showinfo("Game Over", "It's a draw!")
        self.reset_game()

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def reset_game(self):
        for row in self.buttons:
            for button in row:
                button['text'] = ''
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

        if self.vs_computer and self.current_player == 'O':
            self.make_computer_move()

    def make_computer_move(self):
        best_score, best_move = self.minimax(self.board, 0, True)
        self.board[best_move[0]][best_move[1]] = 'O'
        self.buttons[best_move[0]][best_move[1]]['text'] = 'O'

        if self.check_winner():
            self.show_winner()
        elif self.is_board_full():
            self.show_draw()
        else:
            self.switch_player()

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner():
            return -1 if self.current_player == 'X' else 1, None

        if self.is_board_full():
            return 0, None

        moves = []

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O' if is_maximizing else 'X'
                    score, _ = self.minimax(board, depth + 1, not is_maximizing)
                    board[i][j] = ' '

                    moves.append((score, (i, j)))

        if is_maximizing:
            return max(moves, key=lambda x: x[0])
        else:
            return min(moves, key=lambda x: x[0])

    def run(self):
        self.mode_selection_window.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI()
    game.run()
