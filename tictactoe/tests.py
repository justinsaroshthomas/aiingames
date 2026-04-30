"""
Unit Tests for Tic-Tac-Toe Game and Minimax AI
===============================================
Comprehensive test suite verifying game logic correctness
and AI optimality.

Author: Justin Sarosh Thomas
"""

import unittest
from game import TicTacToe
from ai import MinimaxAI


class TestTicTacToe(unittest.TestCase):
    """Tests for the TicTacToe game engine."""

    def setUp(self):
        """Create a fresh game for each test."""
        self.game = TicTacToe()

    def test_initial_state(self):
        """Board should start empty with X as current player."""
        self.assertEqual(self.game.board, [' '] * 9)
        self.assertEqual(self.game.current_player, 'X')
        self.assertEqual(self.game.move_count, 0)

    def test_valid_move(self):
        """Making a valid move should place the mark and increment count."""
        self.assertTrue(self.game.make_move(0))
        self.assertEqual(self.game.board[0], 'X')
        self.assertEqual(self.game.move_count, 1)

    def test_invalid_move_occupied(self):
        """Cannot place a mark on an occupied cell."""
        self.game.make_move(0)
        self.assertFalse(self.game.make_move(0))

    def test_invalid_move_out_of_bounds(self):
        """Cannot place a mark outside the board."""
        self.assertFalse(self.game.make_move(-1))
        self.assertFalse(self.game.make_move(9))

    def test_switch_player(self):
        """Switching should toggle between X and O."""
        self.assertEqual(self.game.current_player, 'X')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'O')
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 'X')

    def test_row_win(self):
        """Detect a horizontal win."""
        self.game.board = ['X', 'X', 'X',
                           'O', 'O', ' ',
                           ' ', ' ', ' ']
        self.game.move_count = 5
        self.assertEqual(self.game.check_winner(), 'X')

    def test_column_win(self):
        """Detect a vertical win."""
        self.game.board = ['O', 'X', ' ',
                           'O', 'X', ' ',
                           'O', ' ', ' ']
        self.game.move_count = 5
        self.assertEqual(self.game.check_winner(), 'O')

    def test_diagonal_win(self):
        """Detect a diagonal win."""
        self.game.board = ['X', 'O', ' ',
                           ' ', 'X', 'O',
                           ' ', ' ', 'X']
        self.game.move_count = 5
        self.assertEqual(self.game.check_winner(), 'X')

    def test_draw(self):
        """Detect a draw when all cells are filled with no winner."""
        self.game.board = ['X', 'O', 'X',
                           'X', 'O', 'O',
                           'O', 'X', 'X']
        self.game.move_count = 9
        self.assertIsNone(self.game.check_winner())
        self.assertTrue(self.game.is_draw())

    def test_available_moves(self):
        """Should return all empty cell positions."""
        self.game.board = ['X', ' ', 'O',
                           ' ', 'X', ' ',
                           'O', ' ', ' ']
        self.assertEqual(self.game.get_available_moves(), [1, 3, 5, 7, 8])

    def test_reset(self):
        """Reset should clear the board completely."""
        self.game.make_move(0)
        self.game.reset()
        self.assertEqual(self.game.board, [' '] * 9)
        self.assertEqual(self.game.move_count, 0)


class TestMinimaxAI(unittest.TestCase):
    """Tests for the Minimax AI algorithm."""

    def setUp(self):
        """Create a fresh game and AI."""
        self.game = TicTacToe()
        self.ai = MinimaxAI(ai_player='O')

    def test_ai_blocks_winning_move(self):
        """AI should block the human's winning move."""
        # X has two in a row, AI must block
        self.game.board = ['X', 'X', ' ',
                           'O', ' ', ' ',
                           ' ', ' ', ' ']
        self.game.move_count = 3
        self.game.current_player = 'O'
        move = self.ai.get_best_move(self.game)
        self.assertEqual(move, 2)  # Must block at position 2

    def test_ai_takes_winning_move(self):
        """AI should take its own winning move when available."""
        self.game.board = ['X', 'X', ' ',
                           'O', 'O', ' ',
                           'X', ' ', ' ']
        self.game.move_count = 5
        self.game.current_player = 'O'
        move = self.ai.get_best_move(self.game)
        self.assertEqual(move, 5)  # O should win at position 5

    def test_ai_never_loses(self):
        """AI should never lose — at worst it draws."""
        # Simulate all possible first moves for X, AI should never lose
        for first_move in range(9):
            game = TicTacToe()
            ai = MinimaxAI(ai_player='O')
            game.make_move(first_move)  # X moves
            game.switch_player()

            while not game.is_game_over():
                if game.current_player == 'O':
                    move = ai.get_best_move(game)
                    game.make_move(move)
                else:
                    # Simulate human playing random available moves
                    moves = game.get_available_moves()
                    if moves:
                        game.make_move(moves[0])
                game.switch_player()

            winner = game.check_winner()
            self.assertNotEqual(
                winner, 'X',
                f"AI lost when X started at position {first_move}"
            )

    def test_ai_takes_center_on_empty_board(self):
        """On an empty board, AI should consider center as strong move."""
        ai_first = MinimaxAI(ai_player='X')
        move = ai_first.get_best_move(self.game)
        # Center (4) or corner (0,2,6,8) are both optimal opening moves
        self.assertIn(move, [0, 2, 4, 6, 8])

    def test_nodes_evaluated_counter(self):
        """AI should track the number of nodes evaluated."""
        self.ai.get_best_move(self.game)
        self.assertGreater(self.ai.nodes_evaluated, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
