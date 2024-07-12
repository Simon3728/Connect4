"""
This file implements two versions of the Minimax algorithm with different heuristics for the Connect 4 game.
The MinimaxPlayer class uses an modified heuristic evaluation function from scientific paper to optimize the move selection process.
The MinimaxPlayer2 class uses a custom heuristic and bitboard representation for faster evaluation of board states.
These implementations allow comparison of different heuristics to evaluate their effectiveness in the game.
"""

from game.player import Player
import random 

class MinimaxPlayer(Player):
    """
    MinimaxPlayer implements the Minimax algorithm with alpha-beta pruning
    to optimize heuristic values for Connect 4. This player can be compared 
    with MinimaxPlayer3 (more basic version of the heuristic) to evaluate the improvements in heuristic evaluation.
    """
    def __init__(self, name, piece, depth=5):
        """
        Initialize the MinimaxPlayer with a name, piece, and search depth.
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
                    score += self.evaluate_window(window, piece, depth)
                    if col >= 1:
                        window2 = row_array[col-1:col + 4]
                        score += self.evaluate_window_win(window2, piece, depth)

            # Score Vertical
            for col in range(board.columns):
                col_array = [board.board[row][col] for row in range(board.rows)]
                for row in range(board.rows - 3):
                    window = col_array[row:row + 4]
                    score += self.evaluate_window(window, piece, depth)

            # Score positive sloped diagonal
            for row in range(board.rows - 3):
                for col in range(board.columns - 3):
                    window = [board.board[row + i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece, depth)
                    if row >= 1 and col >= 1:
                        window.insert(0, board.board[row - 1][col - 1])
                        score += self.evaluate_window_win(window, piece, depth)

            # Score negative sloped diagonal
            for row in range(board.rows - 3):
                for col in range(board.columns - 3):
                    window = [board.board[row + 3 - i][col + i] for i in range(4)]
                    score += self.evaluate_window(window, piece, depth)
                    if row >= 1 and col <= 2:
                        window.insert(0, board.board[row - 1][col + 4])
                        score += self.evaluate_window_win(window, piece, depth)
            return score

        score = score_position(board, self.piece)
        opponent_piece = 2 if self.piece == 1 else 1
        score -= score_position(board, opponent_piece)
        return score

    def evaluate_window(self, window, piece, depth):
        """
        Evaluate a window (subset of the board) heuristically.
        """
        score = 0
        opponent_piece = 2 if piece == 1 else 1

        if window.count(piece) == 4:
            score += 10000000000 * (1/(depth+1))  # Winning move, no depth factor needed
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 900000  # Potential win in one move
            if depth == 1:
                score += 10000000000000000
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 50000  # Potential setup for future win
        elif window.count(piece) == 1 and window.count(0) == 3:
            score += 10000  # Minimal but positive setup
        elif window.count(opponent_piece) == 3 and window.count(0) == 1:
            if depth == 1:
                score -= 20000000000 * (1/(depth+1))  # Blocking opponent's win

        return score

    def evaluate_window_win(self, window, piece, depth):
        """
        Evaluate a window for potential winning moves.
        """
        score = 0
        opponent_piece = 2 if piece == 1 else 1
        if window.count(piece) == 3 and window[0] == 0 and window[4] == 0:
            return 10000000000 * (1/(depth+1)) 
        elif window.count(opponent_piece) == 3 and window[0] == 0 and window[4] == 0:
            if depth == 1:
                score -= 20000000000 * (1/(depth+1))  # Blocking opponent's win
        
        return 0
    
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

class MinimaxPlayer2:
    """
    MinimaxPlayer2 uses a different heuristic and bitboard representation for 
    faster evaluation of Connect 4 board states.
    """
    def __init__(self, name, piece, depth=5, win_score=1000000, threat_score=500000, center_score=5, two_in_row_score=20, three_in_row_score=200, block_opponent_score=1500, diagonal_score=350):
        """
        Initialize the MinimaxPlayer2 with a name, piece, depth, and heuristic scores.
        """
        self.name = name
        self.piece = piece
        self.depth = depth
        self.win_score = win_score
        self.threat_score = threat_score
        self.center_score = center_score
        self.two_in_row_score = two_in_row_score
        self.three_in_row_score = three_in_row_score
        self.block_opponent_score = block_opponent_score
        self.diagonal_score = diagonal_score

    def binary_search_ignore_last_digit(self, filename, target):
        """
        Perform a binary search on a sorted file of numbers, ignoring the last digit of each number during comparison.
        """
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            numbers = [int(line) for line in lines]

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
        
    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        """
        Minimax algorithm with alpha-beta pruning and custom heuristic.
        """
        if depth == 0 or board.is_terminal_node():
            return self.evaluate_board(board)

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
        Get the best move for the player using the Minimax algorithm with custom heuristic.
        """
        turn = board.get_move_count()
        if turn == 0:
            return 3
        elif turn <= 4:
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
                # Print the score for debugging purposes
                print(f"Move: {col}, Score: {value}")
                if value > best_value:
                    best_value = value
                    best_moves = [col]
                elif value == best_value:
                    best_moves.append(col)
                alpha = max(alpha, value)
        return random.choice(best_moves)

    def evaluate_board(self, board):
        """
        Evaluate the board state heuristically using bitboard representation.
        """
        player_bitboard = board.get_bitboard(self.piece)
        opponent_piece = 2 if self.piece == 1 else 1
        opponent_bitboard = board.get_bitboard(opponent_piece)
        return self.evaluate_bitboard(player_bitboard, opponent_bitboard)

    def evaluate_bitboard(self, player_bitboard, opponent_bitboard):
        """
        Evaluate the bitboard representation of the board state heuristically.
        """
        def score_position(bitboard, piece_bitboard):
            score = 0

            # Score Horizontal
            for row in range(6):
                for col in range(4):
                    window = (bitboard >> (row * 7 + col)) & 0b1111
                    score += self.evaluate_window(window, piece_bitboard)

            # Score Vertical
            for col in range(7):
                for row in range(3):
                    window = (bitboard >> (row * 7 + col)) & 0b1000100010001
                    score += self.evaluate_window(window, piece_bitboard)

            # Score positive sloped diagonal
            for row in range(3):
                for col in range(4):
                    window = (bitboard >> (row * 7 + col)) & 0b1000000100000010000001
                    score += self.evaluate_window(window, piece_bitboard)

            # Score negative sloped diagonal
            for row in range(3):
                for col in range(4):
                    window = (bitboard >> (row * 7 + 3 + col)) & 0b10000010000010001
                    score += self.evaluate_window(window, piece_bitboard)

            return score

        player_score = score_position(player_bitboard, player_bitboard)
        opponent_score = score_position(opponent_bitboard, opponent_bitboard)
        return player_score - opponent_score

    def evaluate_window(self, window, piece_bitboard):
        """
        Evaluate a window (subset of the bitboard) heuristically.
        """
        score = 0
        opponent_bitboard = ~piece_bitboard

        # Absolute win
        if window == 0b1111:
            return self.win_score

        # Three in a row (with one empty spot)
        if bin(window).count('1') == 3 and bin(window).count('0') == 1:
            score += self.threat_score

        # Two in a row (with two empty spots)
        if bin(window).count('1') == 2 and bin(window).count('0') == 2:
            score += self.two_in_row_score

        # Single piece
        if bin(window).count('1') == 1:
            score += self.center_score

        # Blocking opponent's win
        if bin(opponent_bitboard & window).count('1') == 3 and bin(window).count('0') == 1:
            score += self.block_opponent_score

        # Specific diagonal threat detection
        if self.is_diagonal(window):
            score += self.diagonal_score

        return score

    def is_diagonal(self, window):
        """
        Check if a window represents a diagonal threat.
        """
        diagonal_patterns = [0b1000, 0b0100, 0b0010, 0b0001]
        for pattern in diagonal_patterns:
            if window & pattern == pattern:
                return True
        return False
