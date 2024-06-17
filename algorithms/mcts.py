# mcts_player.py

import random
import math

class MCTSNode:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.untried_moves = board.get_legal_moves()

    def select_child(self):
        return sorted(self.children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]

    def add_child(self, move, board):
        child = MCTSNode(board, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

class MCTSPlayer:
    def __init__(self, name, piece, iterations=1000):
        self.name = name
        self.piece = piece
        self.iterations = iterations

    def get_move(self, board):
        root = MCTSNode(board)

        for _ in range(self.iterations):
            node = root
            state = board.copy()

            # Select
            while node.untried_moves == [] and node.children != []:
                node = node.select_child()
                state.apply_move(node.move, self.piece if state.get_next_open_row(node.move) % 2 == 0 else 'X' if self.piece == 'O' else 'O')

            # Expand
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                state.apply_move(move, self.piece if state.get_next_open_row(move) % 2 == 0 else 'X' if self.piece == 'O' else 'O')
                node = node.add_child(move, state)

            # Simulate
            piece = self.piece
            while not state.is_terminal_node():
                state.apply_move(random.choice(state.get_legal_moves()), piece)
                piece = 'X' if piece == 'O' else 'O'

            # Backpropagate
            result = 1 if state.check_winner(self.piece) else 0
            while node is not None:
                node.update(result)
                node = node.parent

        return sorted(root.children, key=lambda c: c.visits)[-1].move
