## My Games

This is a collection of games and algorithm projects I programmed mostly around
2020–2021, lightly restored so they are pleasant to play in a browser at
[games.rithwikg.com](https://games.rithwikg.com).

The original Python/Pygame sources remain in their project folders. For the
turn-based games, Snake, Snake AI, and Rubik's Cube, the site calls the original
algorithms on the Flask/Python side and uses a thin browser layer for drawing and
input. The remaining real-time projects keep their original mechanics while
browser-specific adapters provide responsive keyboard and touch input.

### Included

- Connect Four engine with minimax and alpha-beta pruning
- Snake and the Hamiltonian-cycle Snake AI
- Hangman
- Rubik's Cube workbench
- Space Invaders
- Tic-Tac-Toe with minimax
- Sorting algorithm visualizer
- Pathfinding algorithm visualizer

### Run locally

```sh
python3 -m pip install -r requirements.txt
python3 server.py
```

Then open `http://127.0.0.1:5000`.
