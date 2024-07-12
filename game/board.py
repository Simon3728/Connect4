"""
This file defines the Board class for the Connect 4 game. It includes methods for managing the game board, 
such as dropping pieces, checking for valid moves, resetting the board, printing the board, and checking for winners. 
Additional methods are provided for more advanced functionality, including support for Monte Carlo Tree Search (MCTS) 
and encoding the board state to a bitstring.
"""

import numpy as np

class Board:
    def __init__(self, rows=6, columns=7):
        """
        Initialize the game board with the specified number of rows and columns.
        """
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns))

    def drop_piece(self, col, piece):
        """
        Drop a piece into the specified column.
        """
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = piece
                return row, col
        raise ValueError("Column is full")
    
    def is_valid_move(self, col):
        """
        Check if a move is valid (i.e., the column is not full).
        """
        return self.board[0][col] == 0

    def reset(self):
        """
        Reset the board to its initial state (all zeros).
        """
        self.board = np.zeros((self.rows, self.columns))

    def print_board(self):
        """
        Print the board to the console.
        """
        for row in self.board:
            print(''.join(str(int(cell)) for cell in row))
        print('-' * (2 * self.columns - 1))

    def check_winner(self, piece):
        """
        Check if the specified piece has won the game.
        """
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

    def get_state(self):
        """
        Get the current state of the board as a flattened array.
        """
        return self.board.flatten()

    def get_move_count(self):
        """
        Get the number of moves made so far.
        """
        flatten_board = self.get_state()
        return np.count_nonzero(flatten_board)

    def reverse_rows(self):
        """
        Reverse the rows of the board.
        """
        return np.flip(self.board, 0)
    
    def check_draw(self):
        """
        Check if the game is a draw (i.e., the board is full).
        """
        return not np.any(self.board == 0)

    # Additional methods for MCTS
    def copy(self):
        """
        Create a copy of the board.
        """
        new_board = Board(self.rows, self.columns)
        new_board.board = np.copy(self.board)
        return new_board

    def apply_move(self, column, piece):
        """
        Apply a move to the board.
        """
        if self.is_valid_move(column):
            row = self.get_next_open_row(column)
            self.board[row][column] = piece
            return True
        return False

    def get_legal_moves(self):
        """
        Get a list of all legal moves.
        """
        return [c for c in range(self.columns) if self.is_valid_move(c)]

    def is_terminal_node(self):
        """
        Check if the board is in a terminal state (win, lose, or draw).
        """
        return self.check_winner(1) or self.check_winner(2) or len(self.get_legal_moves()) == 0
    
    def get_next_open_row(self, column):
        """
        Get the next open row in the specified column.
        """
        for row in range(self.rows):
            if self.board[row][column] == 0:
                return row

    def get_bitboard(self, piece):
        """
        Get the bitboard representation of the board for the specified piece.
        """
        bitboard = 0
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == piece:
                    bitboard |= 1 << (row * self.columns + col)
        return bitboard

    def set_board_from_bitboard(self, bitboard, piece):
        """
        Set the board state from a bitboard representation.
        """
        for row in range(self.rows):
            for col in range(self.columns):
                if bitboard & (1 << (row * self.columns + col)):
                    self.board[row][col] = piece

    def encode_state(self):
        """
        Encode the board state into a format suitable for neural networks.
        """
        return np.stack((self.board == 1, self.board == 2, self.board == 0)).astype(np.float32)
    
    def get_valid_moves(self):
        """
        Get a list of all valid moves (columns that are not full).
        """
        return [col for col in range(self.columns) if self.is_valid_move(col)]
