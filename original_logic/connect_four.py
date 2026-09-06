"""Loads the algorithm functions directly from Connect4/main.py.

Pygame is replaced by an inert import stub because the Flask process never uses
the original drawing functions. The minimax and rule functions are executed
from the original module without being rewritten here.
"""

import copy
import importlib.util
import sys
import types
from pathlib import Path


def _load_original():
    previous = sys.modules.get("pygame")
    sys.modules["pygame"] = types.ModuleType("pygame")
    try:
        path = Path(__file__).resolve().parents[1] / "Connect4" / "main.py"
        spec = importlib.util.spec_from_file_location("rithwik_connect_four", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if previous is None:
            sys.modules.pop("pygame", None)
        else:
            sys.modules["pygame"] = previous


original = _load_original()


def empty_board():
    return [[0, 0, 0, 0, 0, 0, 0] for _ in range(6)]


def drop(board, player, column):
    return original.check_guess(player, column + 1, board)


def winner(board):
    if original.check_win(1, board, False):
        return 1
    if original.check_win(2, board, False):
        return 2
    if all(all(row) for row in board):
        return 3
    return 0


def computer_move(board, turn, depth=7):
    original.winVal = 10_000_000_000_000
    original.transpositionTable = {}
    result = original.minimax(copy.deepcopy(board), depth, True, -float("inf"), float("inf"), turn)
    return result[1] - 1
