# Restoration notes

The site is a browser presentation layer around old Python projects. The original
files in `Documents/Coding/Python` were treated as read-only references; none were
edited. Original sources already in this repository received only import guards
and small headless/browser hooks.

## Included from the original games repository

| Web project | Original source | What was kept |
| --- | --- | --- |
| Connect Four | `Connect4/main.py` | Flask executes the original board rules, center-first minimax, and alpha-beta pruning directly |
| Snake / Snake AI | `Snake/main.py`, `SnakeAI/main.py` | Flask owns the original 20×20 state, movement, apples, and active Hamiltonian shortcut logic |
| Hangman | `Hangman/main.py` | Local two-player setup and nine-stage drawing |
| Rubik’s Cube | `RubiksCube/main.py` | Flask executes the original Piece model, turns, and `solve3x3`; canvas replaces only PyOpenGL drawing |

## Added from the Python archive

| Web project | Read-only source used | What was kept |
| --- | --- | --- |
| Space Invaders | `Pygame/Space-Invaders/Space_Invaders.py` | Six enemies, horizontal bounce/drop, one-shot firing and respawn scoring |
| Tic-Tac-Toe | `Games/Tic Tac Toe/TicTacToePygameNew.py` | Original minimax and alpha-beta functions extracted verbatim for the Python backend |
| Sorting Lab | `Algorithms Visualizations/Sorting Algorithms/sorting.py` | Bubble, selection, insertion, merge and quicksort |
| Pathfinding Lab | `Algorithms Visualizations/Pathfinding-Algorithm/pathfinding.py` | A*, Dijkstra, BFS, DFS, greedy search and generated mazes |

## Reviewed but not ported in this pass

- The Tetris file is a short board prototype rather than a finished game loop.
- Chess and the socket games need a deeper multiplayer/rules pass to preserve
  their behavior faithfully.
- The NEAT demos depend on training assets and are better shown later as recorded
  experiments with an optional live simulation.
- Hardware, webcam, Discord, data-pipeline, and research projects are not safe or
  useful as direct client-side ports. They would work better as small case-study
  pages with curated outputs rather than pretending to be browser apps.

## Browser changes

- Removed unreliable Pygbag iframe startup from the active routes.
- Added Python-backed JSON adapters for Connect Four, Tic-Tac-Toe, Snake, Snake AI, and the cube solver.
- Added responsive keyboard, pointer, and touch input where appropriate.
- Added explicit ready, pause, win/loss, and restart states.
- Kept the old `/Connect4/play`, `/Snake/play`, `/SnakeAI/play`, `/Hangman/play`,
  and `/RubiksCube/play` URLs as permanent redirects.
