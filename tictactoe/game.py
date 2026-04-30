"""
Tic-Tac-Toe Game Engine
=======================
Core game logic for the Tic-Tac-Toe board, handling moves,
win detection, and game state management.

Author: Justin Sarosh Thomas
"""

from typing import Optional


class TicTacToe:
    """
    Represents a Tic-Tac-Toe game board and provides methods
    for game state management.

    The board is represented as a list of 9 cells (indices 0-8):
        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8

    Each cell can be:
        ' ' - empty
        'X' - player X
        'O' - player O
    """

    # All possible winning combinations (rows, columns, diagonals)
    WINNING_COMBOS = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]

    def __init__(self):
        """Initialize an empty 3x3 board."""
        self.board: list[str] = [' '] * 9
        self.current_player: str = 'X'  # X always goes first
        self.move_count: int = 0

    def make_move(self, position: int) -> bool:
        """
        Place the current player's mark at the given position.

        Args:
            position: Board index (0-8) where the mark should be placed.

        Returns:
            True if the move was valid and executed, False otherwise.
        """
        if not self._is_valid_move(position):
            return False

        self.board[position] = self.current_player
        self.move_count += 1
        return True

    def undo_move(self, position: int) -> None:
        """
        Remove a mark from the given position (used by AI for backtracking).

        Args:
            position: Board index (0-8) to clear.
        """
        self.board[position] = ' '
        self.move_count -= 1

    def switch_player(self) -> None:
        """Toggle between player X and player O."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self) -> Optional[str]:
        """
        Check if there is a winner on the current board.

        Returns:
            'X' if X wins, 'O' if O wins, None if no winner yet.
        """
        for combo in self.WINNING_COMBOS:
            a, b, c = combo
            if (self.board[a] != ' ' and
                    self.board[a] == self.board[b] == self.board[c]):
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        """
        Check if the game is a draw (all cells filled, no winner).

        Returns:
            True if the game is a draw, False otherwise.
        """
        return self.move_count == 9 and self.check_winner() is None

    def is_game_over(self) -> bool:
        """
        Check if the game has ended (either by win or draw).

        Returns:
            True if the game is over, False otherwise.
        """
        return self.check_winner() is not None or self.is_draw()

    def get_available_moves(self) -> list[int]:
        """
        Get all empty positions on the board.

        Returns:
            List of available board indices.
        """
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def _is_valid_move(self, position: int) -> bool:
        """
        Validate that a move can be made at the given position.

        Args:
            position: Board index to validate.

        Returns:
            True if the position is valid and empty, False otherwise.
        """
        return 0 <= position <= 8 and self.board[position] == ' '

    def display(self) -> str:
        """
        Generate a string representation of the current board state.

        Returns:
            Formatted string showing the board with row/column dividers.
        """
        rows = []
        for i in range(0, 9, 3):
            cells = []
            for j in range(3):
                cell = self.board[i + j]
                cells.append(f' {cell} ')
            rows.append('|'.join(cells))

        separator = '───┼───┼───'
        return f'\n{separator}\n'.join(rows)

    def reset(self) -> None:
        """Reset the board to its initial empty state."""
        self.board = [' '] * 9
        self.current_player = 'X'
        self.move_count = 0

    def __repr__(self) -> str:
        return f'TicTacToe(moves={self.move_count}, current={self.current_player})'
