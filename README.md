# 🎮 AI in Games — Tic-Tac-Toe Minimax AI

> Showcasing AI and software projects including a Tic-Tac-Toe AI using the Minimax algorithm. Demonstrates Python programming, algorithm design, game theory, and version control.

![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-f7df1e?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-16%20Passing-22c55e?style=flat-square)

---

## 🧠 About

This project features an **unbeatable Tic-Tac-Toe AI** powered by the **Minimax algorithm** with **Alpha-Beta pruning**. It includes:

- **Python implementation** — Clean, well-documented game engine and AI
- **Interactive web demo** — Play against the AI in your browser
- **Comprehensive tests** — 16 unit tests covering game logic and AI optimality
- **Algorithm visualization** — Real-time stats showing nodes evaluated, pruning, and think time

## 🏗️ Project Structure

```
aiingames/
├── tictactoe/                # Python implementation
│   ├── game.py               # Game engine — board state, moves, win detection
│   ├── ai.py                 # Minimax AI with Alpha-Beta pruning
│   ├── main.py               # Terminal game interface (colored output)
│   └── tests.py              # 16 unit tests
├── docs/                     # Web showcase (GitHub Pages)
│   ├── index.html            # Showcase website
│   ├── style.css             # Premium dark theme styling
│   └── app.js                # Browser game + Minimax AI (JavaScript)
└── README.md
```

## 🚀 Getting Started

### Play in the Browser
Visit the **[Live Demo](https://justinsaroshthomas.github.io/aiingames/)** — no installation required.

### Run the Python Version

```bash
# Clone the repository
git clone https://github.com/justinsaroshthomas/aiingames.git
cd aiingames/tictactoe

# Play against the AI
python main.py

# Run the test suite
python -m unittest tests -v
```

## 🎯 The Minimax Algorithm

The AI uses **Minimax with Alpha-Beta pruning** — a classic decision-making algorithm from game theory.

### How It Works

1. **Game Tree Exploration** — Recursively explores every possible game state
2. **Score Evaluation** — Terminal states receive scores:
   - `+10 - depth` → AI wins (prefers faster wins)
   - `-10 + depth` → Human wins (delays losses)
   - `0` → Draw
3. **Maximize/Minimize** — AI maximizes its score; assumes opponent minimizes it
4. **Alpha-Beta Pruning** — Eliminates irrelevant branches, reducing computation by ~50%

### Pseudocode

```python
def minimax(game, depth, is_maximizing, alpha, beta):
    if terminal_state:
        return evaluate(game, depth)
    
    if is_maximizing:  # AI's turn
        best = -∞
        for move in available_moves:
            score = minimax(game, depth+1, False, alpha, beta)
            best = max(best, score)
            alpha = max(alpha, score)
            if beta <= alpha: break  # Prune!
        return best
    else:  # Human's turn
        best = +∞
        for move in available_moves:
            score = minimax(game, depth+1, True, alpha, beta)
            best = min(best, score)
            beta = min(beta, score)
            if beta <= alpha: break  # Prune!
        return best
```

### Key Facts

| Metric | Value |
|--------|-------|
| Possible game states | 549,946 |
| AI loss rate | 0% (unbeatable) |
| Time complexity | O(b^d) |
| Space complexity | O(d) |
| Pruning efficiency | ~50% reduction |

## 🧪 Test Suite

All **16 tests** pass, covering:

| Category | Tests | Description |
|----------|-------|-------------|
| Game Logic | 10 | Board state, moves, win detection, draws |
| AI Optimality | 5 | Blocking, winning, never losing |
| Performance | 1 | Node evaluation counting |

```bash
$ python -m unittest tests -v

test_ai_blocks_winning_move ... ok
test_ai_never_loses ... ok
test_ai_takes_center_on_empty_board ... ok
test_ai_takes_winning_move ... ok
test_nodes_evaluated_counter ... ok
test_available_moves ... ok
test_column_win ... ok
test_diagonal_win ... ok
test_draw ... ok
test_initial_state ... ok
test_invalid_move_occupied ... ok
test_invalid_move_out_of_bounds ... ok
test_reset ... ok
test_row_win ... ok
test_switch_player ... ok
test_valid_move ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.181s

OK
```

## 💡 Skills Demonstrated

- **Python Programming** — OOP, type hints, PEP-8, docstrings
- **Algorithm Design** — Minimax with Alpha-Beta pruning optimization
- **Game Theory** — Zero-sum games, Nash equilibrium, perfect information
- **Testing & QA** — Comprehensive unit tests with edge cases
- **Web Development** — Interactive browser game with modern CSS
- **Version Control** — Clean Git history, structured repository

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

**Built by [Justin Sarosh Thomas](https://github.com/justinsaroshthomas)** — Demonstrating practical AI and software development skills.
