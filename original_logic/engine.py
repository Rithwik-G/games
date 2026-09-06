"""Session-oriented adapters used by the website's thin rendering layer."""

from . import connect_four, tic_tac_toe


def new_connect_four():
    board = connect_four.empty_board()
    column = connect_four.computer_move(board, 0)
    connect_four.drop(board, 1, column)
    return {"board": board, "turn": 1, "winner": 0, "engine": "python"}


def play_connect_four(board, turn, column):
    if connect_four.winner(board) or not connect_four.drop(board, 2, column):
        return {"board": board, "turn": turn, "winner": connect_four.winner(board), "engine": "python"}
    turn += 1
    won = connect_four.winner(board)
    if not won:
        ai_column = connect_four.computer_move(board, turn)
        connect_four.drop(board, 1, ai_column)
        turn += 1
        won = connect_four.winner(board)
    return {"board": board, "turn": turn, "winner": won, "engine": "python"}


def new_tic_tac_toe():
    board = [["N" for _ in range(3)] for _ in range(3)]
    move = tic_tac_toe.computer_move(board)
    board[move[0]][move[1]] = "X"
    return {"board": board, "winner": None, "engine": "python"}


def play_tic_tac_toe(board, index):
    row, column = divmod(index, 3)
    if board[row][column] != "N" or tic_tac_toe.checkWin(board)[0]:
        return {"board": board, "winner": tic_tac_toe.checkWin(board)[1], "engine": "python"}
    board[row][column] = "O"
    result = tic_tac_toe.checkWin(board)
    if not result[0] and not tic_tac_toe.checkTie(board):
        move = tic_tac_toe.computer_move(board)
        board[move[0]][move[1]] = "X"
        result = tic_tac_toe.checkWin(board)
    winner = result[1] if result[0] else "draw" if tic_tac_toe.checkTie(board) else None
    return {"board": board, "winner": winner, "engine": "python"}
