"""
This file defines the Monte Carlo Tree Search (MCTS) algorithm for the Connect 4 game.
It includes the MCTSNode class, which represents a node in the MCTS tree, and the MCTSPlayer class,
which implements the MCTS algorithm to select the best move for the player.
"""

import random
import math

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        """
        Initialize a Monte Carlo Tree Search (MCTS) node.
        """
        self.board = board
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = board.get_legal_moves()

    def select_child(self):
        """
        Select a child node with the highest UCT (Upper Confidence Bound for Trees) value.
        """
        return sorted(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]

    def add_child(self, move, board):
        """
        Add a child node for the given move and board state.
        """
        child = MCTSNode(board, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        """
        Update the node's visit count and win count based on the result of a simulation.
        """
        self.visits += 1
        self.wins += result

class MCTSPlayer:
    def __init__(self, name, piece, iterations=1000):
        """
        Initialize a Monte Carlo Tree Search (MCTS) player.
        """
        self.name = name
        self.piece = piece
        self.iterations = iterations

    def get_move(self, board, sequence):
        """
        Get the best move for the player using the MCTS algorithm.
        """
        root = MCTSNode(board)
        turn = board.get_move_count()
        if turn == 0:
            return 3
        elif turn <= 5:
            last_digit = self.binary_search_ignore_last_digit(f'Possible_Moves/moves_{turn}.txt', sequence)
            if last_digit > 0 and last_digit < 8:
                return last_digit - 1
            
        for _ in range(self.iterations):
            node = root
            state = board.copy()

            # Select
            while node.untried_moves == [] and node.children != []:
                node = node.select_child()
                state.apply_move(node.move, self.piece if state.get_next_open_row(node.move) % 2 == 0 else 1 if self.piece == 2 else 2)

            # Expand
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                state.apply_move(move, self.piece if state.get_next_open_row(move) % 2 == 0 else 1 if self.piece == 2 else 2)
                node = node.add_child(move, state)

            # Simulate
            piece = self.piece
            while not state.is_terminal_node():
                state.apply_move(random.choice(state.get_legal_moves()), piece)
                piece = 1 if piece == 2 else 2

            # Backpropagate
            result = 1 if state.check_winner(self.piece) else 0
            while node is not None:
                node.update(result)
                node = node.parent

        return sorted(root.children, key=lambda c: c.visits)[-1].move
    
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
