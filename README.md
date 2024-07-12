# Connect 4 Game with AI

This project involves implementing an AI for playing the Connect 4 game. I experimented with two methods: the MiniMax Algorithm and the Monte Carlo Tree Search. However, only the MiniMax Algorithm performed well.

## MiniMax Algorithm

The MiniMax algorithm is a decision-making tool used in games to determine the best move for a player, assuming the opponent also plays optimally. It's particularly useful in two-player zero-sum games like Connect 4. The algorithm evaluates all possible moves, looking ahead several steps to choose the move that maximizes the player's chances of winning while minimizing the opponent's chances.

### How it Works:
1. **Maximizing and Minimizing Players**: One player is the maximizer, trying to get the highest score, and the other is the minimizer, trying to get the lowest score.
2. **Game Tree**: The algorithm constructs a "game tree" where each node represents a possible game state and each branch represents a possible move.
3. **Recursive Exploration**: The algorithm explores the game tree recursively, alternating between the maximizer and minimizer, evaluating potential outcomes.
4. **Leaf Nodes and Evaluation**: At the maximum depth or terminal game state (win, lose, or draw), the game state is evaluated using a scoring function.
5. **Backtracking and Decision Making**: The algorithm backtracks through the tree, choosing moves that maximize the score for the maximizer and minimize the score for the minimizer.

### Challenges and Heuristics:
- **Computational Complexity**: The game tree can grow exponentially, making it impossible to explore the entire tree.
- **Depth Limitation**: Limiting the tree depth can result in suboptimal decisions.
- **Evaluation Function Quality**: The quality of the evaluation function heavily impacts the algorithm's effectiveness.

To address these challenges, heuristics are used. A heuristic is a simplified evaluation function to estimate the value of a game state without exploring all possible future states. The heuristic evaluates the board state at different levels of the game tree, providing scores that guide the decision-making process.

### My Implementation
I implemented the MiniMax algorithm with a heuristic evaluation function and alpha-beta pruning to optimize decision-making. The heuristic evaluates the board based on:
1. **Absolute Win**: Identifying a winning state.
2. **Three Connected Pieces**: Evaluating potential to complete a four-in-a-row.
3. **Two Connected Pieces**: Evaluating future move potential.
4. **Single Piece**: Evaluating pieces based on their position on the board.

Alpha-beta pruning is used to improve efficiency by reducing the number of nodes evaluated in the game tree.

### First 6 Moves
To improve the algorithm's performance in the early game, I used the first 6 moves from a different AI available [here](https://connect4.gamesolver.org/). I played all possible moves and recorded the results to use in my implementation.

## Conclusion
The MiniMax Algorithm performs well, though it sometimes overlooks immediate winning or losing moves. Despite various adjustments, I couldn't fully resolve this issue. I also implemented a Monte Carlo Tree Search Algorithm, but it didn't perform as well, so I focused on the MiniMax implementation.

You can play against the AI using Pygame by downloading the project and running `pygame_main.py`.
