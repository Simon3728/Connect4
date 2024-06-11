class Player:
    def __init__(self, name, piece):
        self.name = name
        self.piece = piece
    
    def get_move(self, board):
        pass  # This will be overridden by subclasses

class HumanPlayer(Player):
    def get_move(self, board):
        column = int(input(f"{self.name}, enter your move (0-{board.columns-1}): "))
        return column

