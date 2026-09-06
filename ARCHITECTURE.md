# Architecture

The site uses Flask for routing and Python game logic, with HTML, CSS, and Canvas
for the browser interface.

## Python-backed games

- Connect Four: board rules, minimax, and alpha-beta pruning
- Snake / Snake AI: 20×20 state, movement, apples, and Hamiltonian logic
- Tic-Tac-Toe: minimax and alpha-beta pruning
- Rubik’s Cube: Piece model, turns, and `solve3x3`

## Browser games

- Hangman
- Space Invaders
- Sorting Lab
- Pathfinding Lab

Each game includes keyboard, pointer, or touch input as appropriate, plus clear
ready, pause, end, and restart states.
