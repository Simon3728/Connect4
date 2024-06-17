from game.game import Game
from algorithms.minimax import MinimaxPlayer, MinimaxPlayer2
from algorithms.mcts import MCTSPlayer

def play_game(player1, player2, starting_turn):
    game = Game()
    game.current_turn = starting_turn
    while True:
        game.board.print_board()
        if game.current_turn == 'X':
            move = player1.get_move(game.board)
            print('X moved')
        else:
            move = player2.get_move(game.board)
            print('O moved')

        if game.play_turn(move):
            return game.board.board, game.current_turn

def main():
    playerO = MCTSPlayer("MCTSPlayer", 'O', iterations=1000)
    playerX = MinimaxPlayer2("Minimax AI", 'X')

    final_board, winner = play_game(playerO, playerX, 'X')

    # results = []
    # for i in range(10):
    #     starting_turn = 'X' if i % 2 == 0 else 'O'
    #     final_board, winner = play_game(playerO, playerX, starting_turn)
    #     results.append({
    #         "final_board": final_board,
    #         "winner": winner
    #     })

    # # # For printing the amount of wins
    # playerO_wins = 0
    # playerX_wins = 0
    # for r in results:
    #     if r['winner'] == 'O':
    #         playerO_wins += 1
    #     else:
    #         playerX_wins += 1
    # print(f"O wins: {playerO_wins}, X wins: {playerX_wins}")


    # For printing the result boards
    # for i, result in enumerate(results):
    #     print(f"Game {i+1}: Winner - {result['winner']}")
    #     for row in result['final_board']:
    #         print('|'.join(row))
    #     print('-' * 20)

if __name__ == "__main__":
    main()
