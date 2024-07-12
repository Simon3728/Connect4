"""
This file implements a basic version of the Minimax algorithm with heuristic evaluation for the Connect 4 game.
The heuristic used here is based on a scientific paper (https://www.scirp.org/html/1-9601415_90972.htm).
"""

from game.player import Player
import random 

class MinimaxPlayer3(Player):
    """
    MinimaxPlayer3 implements a basic version of the Minimax algorithm with heuristic evaluation for Connect 4.
    """
    def __init__(self, name, piece, depth=3):
        """
        Initialize the MinimaxPlayer3 with a name, piece, and search depth.
        """
        super().__init__(name, piece)
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        """
        Minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 or board.check_winner(1) or board.check_winner(2):
            return self.evaluate_board(board, depth)

        valid_moves = [col for col in range(board.columns) if board.is_valid_move(col)]

        if maximizingPlayer:
            max_eval = -float('inf')
            for col in valid_moves:
                row, _ = board.drop_piece(col, self.piece)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.board[row][col] = 0  
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            opponent_piece = 2 if self.piece == 1 else 1
            for col in valid_moves:
                row, _ = board.drop_piece(col, opponent_piece)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.board[row][col] = 0  
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_move(self, board, sequence):
        """
        Get the best move for the player using the Minimax algorithm.
        """
        turn = board.get_move_count()
        if turn == 0:
            return 3
        elif turn <= 5:
            last_digit = self.binary_search_ignore_last_digit(f'Possible_Moves/moves_{turn}.txt', sequence)
            if last_digit > 0 and last_digit < 8:
                return last_digit - 1
            
        best_moves = []
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        for col in range(board.columns):
            if board.is_valid_move(col):
                row, _ = board.drop_piece(col, self.piece)
                value = self.minimax(board, self.depth - 1, alpha, beta, False)
                board.board[row][col] = 0
                #print(f"Move: {col}, Score: {value}, Best Moves: {best_moves}")
                if value > best_value:
                    best_value = value
                    best_moves = [col]
                elif value == best_value:
                    best_moves.append(col)
                alpha = max(alpha, value)
        return random.choice(best_moves)
    
    def evaluate_board(self, board, depth):
        """
        Evaluate the board state heuristically.
        """
        def score_position(board, piece):
            score = 0

            # Feature 4: Single chessman in different columns
            center_array = [board.board[row][board.columns // 2] for row in range(board.rows)]
            center_count = center_array.count(piece)
            score += center_count * 120  # Center column has higher value

            for col in range(board.columns):
                for row in range(board.rows):
                    if board.board[row][col] == piece:
                        if col in [0, board.columns - 1]:  # Columns a or g
                            score += 40
                        elif col in [1, board.columns - 2]:  # Columns b or f
                            score += 70
                        elif col in [2, board.columns - 3]:  # Columns c or e
                            score += 120
                        else:  # Column d
                            score += 200

            # Score Horizontal
            for row in range(board.rows):
                row_array = [board.board[row][col] for col in range(board.columns)]
                for col in range(board.columns - 3):
                    window = row_array[col:col + 4]
                    score += self.evaluate_window(window, piece)
            
            # Score Vertical
            for col in range(board.columns):
                col_array = [board.board[row][col] for row in range(board.rows)]
                for row in range(board.rows - 3):
                    window = col_array[row:row + 4]
                    score += self.evaluate_window(window, piece)

            # Score positive sloped diagonal
            for row in range(board.rows - 3):
                for col in range(board.columns - 3):
                    window = [board.board[row + i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            # Score negative sloped diagonal
            for row in range(board.rows - 3):
                for col in range(board.columns - 3):
                    window = [board.board[row + 3 - i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            return score

        score = score_position(board, self.piece)
        opponent_piece = 2 if self.piece == 1 else 1
        score -= score_position(board, opponent_piece)
        return score

    def evaluate_window(self, window, piece):
        """
        Evaluate a window (subset of the board) heuristically.
        """
        score = 0

        if window.count(piece) == 4:
            score += 1000000  # Winning move, no depth factor needed
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 900000  # Potential win in one move
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 50000  # Potential setup for future win
        elif window.count(piece) == 1 and window.count(0) == 3:
            score += 10000  # Minimal but positive setup

        return score

    def binary_search_ignore_last_digit(self, filename, target):
        """
        Perform a binary search on a sorted file of numbers, ignoring the last digit of each number during comparison.
        """
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            try:
                numbers = [int(line) for line in lines]
            except:
                return -1
            target_int = int(target)  
            left, right = 0, len(numbers) - 1

            while left <= right:
                mid = (left + right) // 2
                mid_value = numbers[mid] // 10  

                if mid_value == target_int:
                    last_digit = numbers[mid] % 10
                    return last_digit  
                elif mid_value < target_int:
                    left = mid + 1
                else:
                    right = mid - 1
            return -1
