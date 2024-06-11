# This file contains the Board class, which is responsible for managing the state of the game board.

# board.py
class Board:
    def __init__(self, rows=6, columns=7):
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]
    
    def drop_piece(self, column, piece):
        for row in reversed(range(self.rows)):
            if self.board[row][column] == ' ':
                self.board[row][column] = piece
                return row, column
        raise ValueError("Column is full")
    
    def is_valid_move(self, column):
        return self.board[0][column] == ' '
    
    def print_board(self):
        for row in self.board:
            print('|'.join(row))
        print('-' * (2 * self.columns - 1))
    
    def check_winner(self, piece):
        # Horizontal, vertical, and diagonal checks
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True
        
        for row in range(self.rows - 3):
            for col in range(self.columns):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True
        
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == piece for i in range(4)):
                    return True

        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True

        return False

    def reset_board(self):
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

