from game.game import Game
from game.player import HumanPlayer
from algorithms.minimax import MinimaxPlayer

def main():
    game = Game()
    player1 = HumanPlayer("Player 1", 'O')
    player2 = MinimaxPlayer("Minimax AI", 'X')
    
    while True:
        game.board.print_board()
        if game.current_turn == 'X':
            move = player1.get_move(game.board)
        else:
            move = player2.get_move(game.board)
        
        if game.play_turn(move):
            break

if __name__ == "__main__":
    main()