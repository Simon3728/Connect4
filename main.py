"""
Main function to test the efficiency of the different Algorithms and Heuristics
"""
from game.game import Game
from algorithms.minimax import MinimaxPlayer
from algorithms.minimax2 import MinimaxPlayer3

import time

def play_game(player1, player2, starting_turn):
    """
    Simulate a game between two players starting with the specified turn.
    Track the execution time for each player and the sequence of moves made.
    """
    game = Game()
    game.current_turn = starting_turn

    execution1_time, execution2_time = 0, 0
    moves = ''
    while True:
        if game.current_turn == 1:
            start_time = time.time()
            move = player1.get_move(game.board, moves)
            end_time = time.time()
            execution1_time += end_time - start_time
        else:
            start_time = time.time()
            move = player2.get_move(game.board, moves)
            end_time = time.time()
            execution2_time += end_time - start_time
            
        moves += str(move)  # Track the moves made
        
        result = game.play_turn(move)
        if result == 1:
            return game.board.board, game.current_turn, execution1_time, execution2_time
        elif result == -1:
            print("The game is a draw!")
            return game.board.board, -1, execution1_time, execution2_time
        
def main():
    """
    Main function to execute the efficiency tests of the different algorithms.
    It initializes the players, plays multiple games, and prints the results.
    """
    # Create players
    player1 = MinimaxPlayer("MinimaxPlayer", 1, depth=6)
    player2 = MinimaxPlayer3("MinimaxPlayer3", 2, depth=5)

    results = []
    for i in range(50):  # Play 50 games for better evaluation
        starting_turn = 1 if i % 2 == 0 else 2
        print("Game ", i + 1)
        final_board, winner, execution1_time, execution2_time = play_game(player1, player2, starting_turn)
        results.append({
            "final_board": final_board,
            "winner": winner,
            "execution1_time": execution1_time,
            "execution2_time": execution2_time,
        })

    # For printing the amount of wins
    player1_wins = 0
    player2_wins = 0
    draws = 0
    total_time1, total_time2 = 0, 0
    for r in results:
        if r['winner'] == 1:
            player1_wins += 1
        elif r['winner'] == 2:
            player2_wins += 1
        else:
            draws += 1
        total_time1 += r["execution1_time"]
        total_time2 += r["execution2_time"]
    
    print(f"{player1.name} wins: {player1_wins}")
    print(f"{player2.name} wins: {player2_wins}")
    print(f"Draw: {draws}")
    print(f"Total execution time for {player1.name}: {total_time1}")
    print(f"Total execution time for {player2.name}: {total_time2}")

if __name__ == "__main__":
    main()
