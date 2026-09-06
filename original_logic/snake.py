"""Browser-safe state wrapper around the original Snake and SnakeAI loops.

The board coordinates, starting position, apple placement, movement rules, and
Hamiltonian shortcut selection below are retained from ``Snake/main.py`` and
``SnakeAI/main.py``.  Pygame's drawing/event loop is intentionally left to the
browser; this module owns the actual game state and every tick.
"""

from random import randint


BOARD_SIZE = 20


def generate_hamiltonian_path_for_board(board_size):
    # Same sequence as generateHamiltonianPathForBoard in SnakeAI/main.py.
    sequence = []
    for row_pair in range(board_size // 2):
        row = row_pair * 2
        for number in range((board_size * row) + 1, board_size * (row + 1)):
            sequence.append(number)
        for number in range((board_size * (row + 2)) - 1, board_size * (row + 1), -1):
            sequence.append(number)
    for number in range(board_size * board_size - board_size, -1, -board_size):
        sequence.append(number)
    return sequence


PATH = generate_hamiltonian_path_for_board(BOARD_SIZE)


def create_apple(player_positions):
    # Same retry-until-free approach as createApple in both original files.
    x, y = player_positions[0]
    while [x, y] in player_positions:
        x = randint(0, BOARD_SIZE - 1)
        y = randint(0, BOARD_SIZE - 1)
    return [x, y]


def new_game(ai=False):
    state = {
        "snake": [[15, 15], [15, 16], [15, 17]],
        "direction": "up",
        "ai": bool(ai),
        "over": False,
        "won": False,
        "moves": 0,
        "engine": "python",
    }
    state["apple"] = create_apple(state["snake"])
    return state


def _ai_head(state):
    # This is the active curBest block from SnakeAI/main.py, with only names
    # normalized. Its unusual x*20+y numbering is deliberately preserved.
    positions = state["snake"]
    head_number = positions[0][0] * BOARD_SIZE + positions[0][1]
    path_index = PATH.index(head_number)
    apple_number = BOARD_SIZE * state["apple"][0] + state["apple"][1]
    apple_index = PATH.index(apple_number)

    move_numbers = []
    if head_number % BOARD_SIZE != 0:
        move_numbers.append(head_number - 1)
    if head_number % BOARD_SIZE != BOARD_SIZE - 1:
        move_numbers.append(head_number + 1)
    if head_number >= BOARD_SIZE:
        move_numbers.append(head_number - BOARD_SIZE)
    if head_number < BOARD_SIZE * BOARD_SIZE - BOARD_SIZE:
        move_numbers.append(head_number + BOARD_SIZE)

    best = [PATH[(path_index + 1) % (BOARD_SIZE * BOARD_SIZE)], 1]
    tail_index = PATH.index(positions[-1][0] * BOARD_SIZE + positions[-1][1])
    for number in move_numbers:
        position = [number // BOARD_SIZE, number % BOARD_SIZE]
        if not 0 < number < BOARD_SIZE * BOARD_SIZE or position in positions:
            continue
        candidate_index = PATH.index(number)
        if candidate_index > path_index:
            if not (apple_index < candidate_index and apple_index > path_index) and not (
                tail_index <= candidate_index and tail_index >= path_index
            ):
                distance = candidate_index - path_index
                if best[1] < distance:
                    best = [number, distance]
        elif not (apple_index > path_index) and not (apple_index < candidate_index) and not (
            tail_index >= path_index
        ) and not (tail_index <= candidate_index):
            distance = BOARD_SIZE * BOARD_SIZE - path_index + candidate_index
            if best[1] < distance:
                best = [number, distance]
    return [best[0] // BOARD_SIZE, best[0] % BOARD_SIZE]


def tick(state, requested_direction=None):
    if state["over"]:
        return state

    positions = state["snake"]
    if state["ai"]:
        new_head = _ai_head(state)
    else:
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if requested_direction in opposite and requested_direction != opposite[state["direction"]]:
            state["direction"] = requested_direction
        x, y = positions[0]
        dx, dy = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}[
            state["direction"]
        ]
        new_head = [x + dx, y + dy]

    positions.insert(0, new_head)
    if new_head == state["apple"]:
        if len(positions) == BOARD_SIZE * BOARD_SIZE:
            state["over"] = True
            state["won"] = True
        else:
            state["apple"] = create_apple(positions)
    else:
        positions.pop()

    state["moves"] += 1
    if new_head in positions[1:] or new_head[0] in (-1, BOARD_SIZE) or new_head[1] in (-1, BOARD_SIZE):
        state["over"] = True
    return state


def public_state(state):
    return {
        "snake": state["snake"],
        "apple": state["apple"],
        "direction": state["direction"],
        "ai": state["ai"],
        "over": state["over"],
        "won": state["won"],
        "moves": state["moves"],
        "score": max(0, len(state["snake"]) - 3),
        "engine": state["engine"],
    }
