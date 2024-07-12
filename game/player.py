"""
This file defines the Player class and its subclass HumanPlayer for managing player interactions in the Connect 4 game.
The Player class serves as a base class, while the HumanPlayer class handles moves based on mouse input.
"""

import pygame as pg

class Player:
    def __init__(self, name, piece):
        """
        Initialize a player with a name and a piece (1 or 2).
        """
        self.name = name
        self.piece = piece
    
    def get_move(self, board):
        """
        Get the move for the player. This method should be overridden by subclasses.
        """
        pass  # This will be overridden by subclasses

class HumanPlayer(Player):
    def get_move(self, board, padding, squaresize):
        """
        Get the move for a human player by handling mouse input.
        """
        column_ranges = []
        for i in range(board.columns):
            if i == 0:
                start = 0
            else:
                start = i * squaresize + padding
            end = start + squaresize if i != board.columns - 1 else start + squaresize + padding
            column_ranges.append((start, end))

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = None
                for idx, (start, end) in enumerate(column_ranges):
                    if start <= posx <= end:
                        col = idx
                        break

                if col is not None:
                    if board.is_valid_move(col):
                        return col
                else:
                    raise ValueError("Column index out of range")

        return None  
