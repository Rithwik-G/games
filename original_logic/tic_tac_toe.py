"""Logic extracted from Games/Tic Tac Toe/TicTacToePygameNew.py.

The functions below intentionally retain the original board representation,
win checks, transposition table, and alpha-beta minimax structure. Only the
Pygame drawing and mouse-reading functions live in the browser adapter.
"""

import copy


xWin = ["X", "X", "X"]
oWin = ["O", "O", "O"]
transpositionTable = {}


def checkWin(board):
    win = False
    winner = None
    for ind in range(3):
        lst = board[ind]
        if lst == xWin:
            winner = "X"
            win = True
        elif lst == oWin:
            winner = "O"
            win = True

        lst = [board[i][ind] for i in range(3)]
        if lst == xWin:
            winner = "X"
            win = True
        elif lst == oWin:
            winner = "O"
            win = True

    lst = [board[i][i] for i in range(3)]
    if lst == xWin:
        winner = "X"
        win = True
    elif lst == oWin:
        winner = "O"
        win = True

    lst = [board[i][2 - i] for i in range(3)]
    if lst == xWin:
        win = True
        winner = "X"
    elif lst == oWin:
        win = True
        winner = "O"

    return [win, winner]


def checkTie(board):
    for row in board:
        for square in row:
            if square == "N":
                return False
    return True


def convertBoard(board):
    representation = ""
    for row in board:
        for square in row:
            representation += square
    return representation


def minimax(board, depth, maximizingPlayer, alpha, beta):
    win = checkWin(board)
    tie = checkTie(board)
    if win[0] or depth == 0 or tie:
        if win[0]:
            if win[1] == "X":
                return [float("inf"), None, []]
            return [float("-inf"), None, []]
        if tie:
            return [0, None, []]

    boardConversion = convertBoard(board)
    if boardConversion in transpositionTable:
        return transpositionTable[boardConversion]

    if maximizingPlayer:
        value = -float("inf")
        bestMove = None
        movePath = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == "N":
                    newBoard = copy.deepcopy(board)
                    newBoard[row][column] = "X"
                    newVal = minimax(newBoard, depth - 1, not maximizingPlayer, alpha, beta)
                    if newVal[0] > value:
                        value = newVal[0]
                        bestMove = [row, column]
                        movePath = newVal[2]
                        movePath.append([bestMove, value])
                    alpha = max(newVal[0], alpha)
                    if beta <= alpha:
                        transpositionTable[boardConversion] = [value, bestMove, movePath]
                        return [value, bestMove, movePath]
    else:
        value = float("inf")
        bestMove = None
        movePath = []
        for row in range(len(board)):
            for column in range(len(board[row])):
                if board[row][column] == "N":
                    newBoard = copy.deepcopy(board)
                    newBoard[row][column] = "O"
                    newVal = minimax(newBoard, depth - 1, not maximizingPlayer, alpha, beta)
                    if newVal[0] < value:
                        value = newVal[0]
                        bestMove = [row, column]
                        movePath = newVal[2]
                        movePath.append([bestMove, value])
                    beta = min(newVal[0], beta)
                    if beta <= alpha:
                        transpositionTable[boardConversion] = [value, bestMove, movePath]
                        return [value, bestMove, movePath]

    transpositionTable[boardConversion] = [value, bestMove, movePath]
    return [value, bestMove, movePath]


def computer_move(board):
    global transpositionTable
    transpositionTable = {}
    move = minimax(copy.deepcopy(board), 10000, True, float("-inf"), float("inf"))
    return move[1]
