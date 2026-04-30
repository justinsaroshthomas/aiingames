"""
Tic-Tac-Toe — Human vs AI (Terminal Version)
=============================================
A command-line interface for playing Tic-Tac-Toe against
an unbeatable Minimax AI.

Features:
  • Clean terminal display with colored output
  • Move validation and error handling
  • Performance stats (nodes evaluated per move)
  • Option to play as X or O
  • Play-again functionality

Usage:
    python main.py

Author: Justin Sarosh Thomas
"""

import os
import sys
from game import TicTacToe
from ai import MinimaxAI


# ANSI color codes for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Display the game title banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════╗
║       🎮  TIC-TAC-TOE vs MINIMAX AI  🤖  ║
║                                          ║
║    Can you beat the unbeatable?           ║
╚══════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)


def print_board(game: TicTacToe):
    """
    Display the game board with colors and position hints.

    Args:
        game: The current game state.
    """
    print()
    print(f"  {Colors.DIM}Board positions:{Colors.RESET}")
    print(f"  {Colors.DIM}  1 | 2 | 3{Colors.RESET}")
    print(f"  {Colors.DIM}  4 | 5 | 6{Colors.RESET}")
    print(f"  {Colors.DIM}  7 | 8 | 9{Colors.RESET}")
    print()

    for i in range(0, 9, 3):
        row = '  '
        for j in range(3):
            cell = game.board[i + j]
            if cell == 'X':
                row += f' {Colors.BLUE}{Colors.BOLD}X{Colors.RESET} '
            elif cell == 'O':
                row += f' {Colors.RED}{Colors.BOLD}O{Colors.RESET} '
            else:
                row += f' {Colors.DIM}{i + j + 1}{Colors.RESET} '
            if j < 2:
                row += '│'
        print(row)
        if i < 6:
            print(f'  ───┼───┼───')
    print()


def get_human_move(game: TicTacToe) -> int:
    """
    Prompt the human player for a valid move.

    Args:
        game: The current game state.

    Returns:
        A valid board position (0-8).
    """
    while True:
        try:
            move = input(
                f"  {Colors.YELLOW}Your move (1-9): {Colors.RESET}"
            ).strip()

            if move.lower() == 'q':
                print(f"\n  {Colors.DIM}Thanks for playing!{Colors.RESET}\n")
                sys.exit(0)

            position = int(move) - 1  # Convert 1-9 to 0-8

            if position < 0 or position > 8:
                print(f"  {Colors.RED}⚠ Enter a number 1-9{Colors.RESET}")
                continue

            if game.board[position] != ' ':
                print(f"  {Colors.RED}⚠ That position is taken!{Colors.RESET}")
                continue

            return position

        except ValueError:
            print(f"  {Colors.RED}⚠ Please enter a valid number{Colors.RESET}")


def play_game():
    """Run a single game of Tic-Tac-Toe: Human vs AI."""
    clear_screen()
    print_banner()

    # Choose side
    print(f"  {Colors.CYAN}Choose your side:{Colors.RESET}")
    print(f"  {Colors.BLUE}[1] Play as X (go first){Colors.RESET}")
    print(f"  {Colors.RED}[2] Play as O (go second){Colors.RESET}")
    print()

    while True:
        choice = input(f"  {Colors.YELLOW}Enter 1 or 2: {Colors.RESET}").strip()
        if choice in ('1', '2'):
            break
        print(f"  {Colors.RED}⚠ Please enter 1 or 2{Colors.RESET}")

    human_mark = 'X' if choice == '1' else 'O'
    ai_mark = 'O' if human_mark == 'X' else 'X'
    ai = MinimaxAI(ai_player=ai_mark)

    game = TicTacToe()

    print(
        f"\n  {Colors.GREEN}You are "
        f"{Colors.BOLD}{human_mark}{Colors.RESET}"
        f"{Colors.GREEN}, AI is "
        f"{Colors.BOLD}{ai_mark}{Colors.RESET}"
    )

    # Game loop
    while not game.is_game_over():
        print_board(game)

        if game.current_player == human_mark:
            # Human's turn
            move = get_human_move(game)
        else:
            # AI's turn
            print(f"  {Colors.DIM}AI is thinking...{Colors.RESET}")
            move = ai.get_best_move(game)
            print(
                f"  {Colors.CYAN}AI plays position "
                f"{Colors.BOLD}{move + 1}{Colors.RESET}"
                f"  {Colors.DIM}({ai.nodes_evaluated} nodes evaluated)"
                f"{Colors.RESET}"
            )

        game.make_move(move)
        game.switch_player()

    # Game over — show results
    clear_screen()
    print_banner()
    print_board(game)

    winner = game.check_winner()
    if winner == human_mark:
        print(
            f"  {Colors.GREEN}{Colors.BOLD}"
            f"🎉 Congratulations! You won!{Colors.RESET}"
        )
    elif winner == ai_mark:
        print(
            f"  {Colors.RED}{Colors.BOLD}"
            f"🤖 AI wins! The Minimax algorithm is unbeatable.{Colors.RESET}"
        )
    else:
        print(
            f"  {Colors.YELLOW}{Colors.BOLD}"
            f"🤝 It's a draw! Well played.{Colors.RESET}"
        )


def main():
    """Main entry point — supports replay."""
    while True:
        play_game()
        print()
        again = input(
            f"  {Colors.CYAN}Play again? (y/n): {Colors.RESET}"
        ).strip().lower()
        if again != 'y':
            print(f"\n  {Colors.DIM}Thanks for playing! 👋{Colors.RESET}\n")
            break


if __name__ == '__main__':
    main()
