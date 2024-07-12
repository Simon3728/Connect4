"""
This file defines the Game class for managing the Connect 4 game. It includes methods for initializing the game,
playing a turn, and checking for game outcomes such as a win or draw.
"""

from game.board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 1  

    def play_turn(self, column):
        """
        Play a turn in the game by dropping a piece in the specified column for the current player.
        Check for a win or draw after the move.
        """
        piece = 1 if self.current_turn == 1 else 2

        _, _ = self.board.drop_piece(column, piece)
        
        if self.board.check_winner(piece):
            self.board.print_board()
            print(f"Player {piece} wins!")
            return 1
        
        if self.board.check_draw():
            return -1
        
        self.current_turn = 2 if self.current_turn == 1 else 1
        return 0
    
