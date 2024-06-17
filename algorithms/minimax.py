# https://www.scirp.org/html/1-9601415_90972.htm

from game.player import Player
import random 
import math

class MinimaxPlayer2(Player):
    def __init__(self, name, piece, depth=5):
        super().__init__(name, piece)
        self.depth = depth

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.check_winner('X') or board.check_winner('O'):
            return self.evaluate_board(board)

        valid_moves = [col for col in range(board.columns) if board.is_valid_move(col)]

        if maximizingPlayer:
            max_eval = -float('inf')
            for col in valid_moves:
                row, _ = board.drop_piece(col, self.piece)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.board[row][col] = ' '  
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            opponent_piece = 'O' if self.piece == 'X' else 'X'
            for col in valid_moves:
                row, _ = board.drop_piece(col, opponent_piece)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.board[row][col] = ' '  
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def get_move(self, board):
        best_moves = []
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')
        for col in range(board.columns):
            if board.is_valid_move(col):
                row, _ = board.drop_piece(col, self.piece)
                value = self.minimax(board, self.depth - 1, alpha, beta, False)
                board.board[row][col] = ' '  
                if value > best_value:
                    best_value = value
                    best_moves = [col]
                elif value == best_value:
                    best_moves.append(col)
                alpha = max(alpha, value)
        return random.choice(best_moves)
    
    def evaluate_board(self, board):
        def score_position(board, piece):
            score = 0
            
            # Feature 4: Single chessman in different columns
            center_array = [board.board[row][board.columns//2] for row in range(board.rows)]
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
                for col in range(board.columns-3):
                    window = row_array[col:col+4]
                    score += self.evaluate_window(window, piece)
            
            # Score Vertical
            for col in range(board.columns):
                col_array = [board.board[row][col] for row in range(board.rows)]
                for row in range(board.rows-3):
                    window = col_array[row:row+4]
                    score += self.evaluate_window(window, piece)

            # Score positive sloped diagonal
            for row in range(board.rows-3):
                for col in range(board.columns-3):
                    window = [board.board[row+i][col+i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            # Score negative sloped diagonal
            for row in range(board.rows-3):
                for col in range(board.columns-3):
                    window = [board.board[row+3-i][col+i] for i in range(4)]
                    score += self.evaluate_window(window, piece)

            return score

        score = score_position(board, self.piece)
        opponent_piece = 'O' if self.piece == 'X' else 'X'
        score -= score_position(board, opponent_piece)
        return score

    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = 'O' if piece == 'X' else 'X'
        
        if window.count(piece) == 4:
            score += float('inf')  # Feature 1: Absolute win
        elif window.count(piece) == 3 and window.count(' ') == 1:
            if self.has_adjacent_space(window):  # Feature 2: Three connected with adjacent space
                score += float('inf')
            else:
                score += 900000
        elif window.count(piece) == 2 and window.count(' ') == 2:
            if self.has_adjacent_space(window):  # Feature 3: Two connected with adjacent space
                score += 50000
            else:
                # Assign score based on number of available squares
                available_squares = window.count(' ')
                if available_squares == 5:
                    score += 40000
                elif available_squares == 4:
                    score += 30000
                elif available_squares == 3:
                    score += 20000
                elif available_squares == 2:
                    score += 10000

        if window.count(opponent_piece) == 3 and window.count(' ') == 1:
            score -= 900000  # Significant penalty for opponent's three in a row with adjacent space
        elif window.count(opponent_piece) == 2 and window.count(' ') == 2:
            score -= 50000  # Penalty for opponent's two in a row with adjacent space

        return score

    def has_adjacent_space(self, window):
        return ' ' in window

