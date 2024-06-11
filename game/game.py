# This file contains the Game class, which manages the overall game logic and flow.

from game.board import Board

class Game:
    def __init__(self):
        self.board = Board()
        self.current_turn = 'X'
    
    def switch_turn(self):
        self.current_turn = 'O' if self.current_turn == 'X' else 'X'
    
    def play_turn(self, column):
        if self.board.is_valid_move(column):
            row, col = self.board.drop_piece(column, self.current_turn)
            if self.board.check_winner(self.current_turn):
                print(f"Player {self.current_turn} wins!")
                return True
            self.switch_turn()
        else:
            print("Invalid move. Try again.")
        return False
    
    def reset_game(self):
        self.board.reset_board()
        self.current_turn = 'X'
