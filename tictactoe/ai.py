"""
Tic-Tac-Toe AI — Minimax Algorithm
====================================
Implementation of an unbeatable Tic-Tac-Toe AI using the Minimax
algorithm with Alpha-Beta pruning for optimal performance.

The Minimax algorithm is a decision-making algorithm used in
game theory and AI. It works by:
  1. Recursively exploring all possible future game states
  2. Assigning scores to terminal states (win/loss/draw)
  3. Choosing the move that maximizes the AI's minimum guaranteed outcome

Alpha-Beta pruning optimizes Minimax by eliminating branches that
cannot influence the final decision, reducing computation time.

Author: Justin Sarosh Thomas
"""

import math
from typing import Optional
from game import TicTacToe


class MinimaxAI:
    """
    An unbeatable Tic-Tac-Toe AI using the Minimax algorithm
    with Alpha-Beta pruning optimization.

    Attributes:
        ai_player: The mark used by the AI ('X' or 'O').
        human_player: The mark used by the human opponent.
        nodes_evaluated: Counter for performance analysis.
    """

    def __init__(self, ai_player: str = 'O'):
        """
        Initialize the AI with a player mark.

        Args:
            ai_player: The mark the AI will use ('X' or 'O').
                       Defaults to 'O' (AI goes second).
        """
        self.ai_player = ai_player
        self.human_player = 'X' if ai_player == 'O' else 'O'
        self.nodes_evaluated = 0

    def get_best_move(self, game: TicTacToe) -> Optional[int]:
        """
        Determine the optimal move for the AI using Minimax.

        This method evaluates all possible moves and returns
        the position that guarantees the best possible outcome
        for the AI player.

        Args:
            game: The current TicTacToe game state.

        Returns:
            The optimal board position (0-8), or None if no
            moves are available (game is over).
        """
        self.nodes_evaluated = 0
        best_score = -math.inf
        best_move = None

        for move in game.get_available_moves():
            # Try this move
            game.board[move] = self.ai_player
            game.move_count += 1

            # Evaluate this move using Minimax
            score = self._minimax(
                game,
                depth=0,
                is_maximizing=False,
                alpha=-math.inf,
                beta=math.inf
            )

            # Undo the move
            game.board[move] = ' '
            game.move_count -= 1

            # Track the best move
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(
        self,
        game: TicTacToe,
        depth: int,
        is_maximizing: bool,
        alpha: float,
        beta: float
    ) -> int:
        """
        The Minimax algorithm with Alpha-Beta pruning.

        Recursively evaluates all possible game states to find
        the optimal score for the current position.

        Algorithm overview:
        ──────────────────
        • MAXIMIZING player (AI): Tries to maximize the score
        • MINIMIZING player (Human): Tries to minimize the score
        • Terminal states are scored as:
            +10 - depth  →  AI wins (prefer faster wins)
            -10 + depth  →  Human wins (prefer slower losses)
            0            →  Draw

        Alpha-Beta pruning:
        ──────────────────
        • Alpha: Best score the maximizer can guarantee
        • Beta: Best score the minimizer can guarantee
        • If alpha >= beta, we prune (skip) that branch

        Args:
            game: Current game state.
            depth: Current depth in the game tree (for move ordering).
            is_maximizing: True if it's the AI's turn to maximize.
            alpha: Best guaranteed score for the maximizer.
            beta: Best guaranteed score for the minimizer.

        Returns:
            The evaluation score of the current position.
        """
        self.nodes_evaluated += 1

        # Check for terminal states
        winner = game.check_winner()
        if winner == self.ai_player:
            return 10 - depth   # AI wins — prefer faster wins
        if winner == self.human_player:
            return -10 + depth  # Human wins — prefer slower losses
        if game.is_draw():
            return 0            # Draw

        if is_maximizing:
            # AI's turn — maximize the score
            max_eval = -math.inf
            for move in game.get_available_moves():
                game.board[move] = self.ai_player
                game.move_count += 1

                eval_score = self._minimax(game, depth + 1, False, alpha, beta)

                game.board[move] = ' '
                game.move_count -= 1

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                # Alpha-Beta pruning: cut off branches that
                # the minimizer would never allow
                if beta <= alpha:
                    break

            return max_eval
        else:
            # Human's turn — minimize the score
            min_eval = math.inf
            for move in game.get_available_moves():
                game.board[move] = self.human_player
                game.move_count += 1

                eval_score = self._minimax(game, depth + 1, True, alpha, beta)

                game.board[move] = ' '
                game.move_count -= 1

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                # Alpha-Beta pruning: cut off branches that
                # the maximizer would never allow
                if beta <= alpha:
                    break

            return min_eval
