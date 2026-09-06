import os
from threading import Lock

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

from original_logic import engine
from original_logic import rubiks_cube
from original_logic import snake


app = Flask(__name__)
app.secret_key = os.environ.get("GAMES_SESSION_KEY", "local-games-development-key")
python_engine_lock = Lock()


PROJECTS = [
    {
        "slug": "connect-four", "title": "Connect Four", "year": "2020", "kind": "game · minimax",
        "description": "The original alpha-beta Connect Four engine, now with a quick browser board and a proper rematch loop.",
        "note": "The computer still prefers the center columns and searches ahead using the original minimax idea.",
        "controls": "Click a column to drop a piece.", "accent": "red",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/Connect4",
    },
    {
        "slug": "snake", "title": "Snake / Snake AI", "year": "2021", "kind": "game · hamiltonian path",
        "description": "Play the 20×20 Snake board yourself, or let the Hamiltonian-cycle AI patiently fill it.",
        "note": "The Python backend runs the original grid, movement, apple, and active Hamiltonian shortcut logic; Canvas only draws each returned state.",
        "controls": "Arrow keys or WASD. Space pauses; R restarts.", "accent": "green",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/SnakeAI",
    },
    {
        "slug": "hangman", "title": "Hangman", "year": "2020", "kind": "game · two player",
        "description": "One person enters a secret phrase, then hands the screen over for the original local two-player game.",
        "note": "The nine-part drawing and pass-the-keyboard format are preserved; the input and end states are simply clearer.",
        "controls": "Type or click letters. R starts a new round.", "accent": "ink",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/Hangman",
    },
    {
        "slug": "rubiks-cube", "title": "Rubik’s Cube", "year": "2021", "kind": "project · cube solver",
        "description": "A compact cube workbench for turning, scrambling, and replaying a solution in the browser.",
        "note": "The original 2,000-line Piece model and solve3x3 routine run in Python; a thin canvas adapter keeps the interactive 3D view browser-friendly.",
        "controls": "Use the face buttons; hold Shift for counter-clockwise turns.", "accent": "blue",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/RubiksCube",
    },
    {
        "slug": "space-invaders", "title": "Space Invaders", "year": "2021", "kind": "game · arcade",
        "description": "The six-enemy arcade loop, rebuilt around the original movement, collision, and respawn rules.",
        "note": "The browser version replaces absolute file paths and adds touch controls, pause, and a clean restart.",
        "controls": "Left/right or A/D to move. Space fires.", "accent": "violet", "source_url": None,
    },
    {
        "slug": "tic-tac-toe", "title": "Tic-Tac-Toe", "year": "2020", "kind": "game · minimax",
        "description": "A tiny, stubborn opponent using the same alpha-beta minimax idea as the original desktop build.",
        "note": "You are O, the computer is X, and—just as in the Python version—the computer opens.",
        "controls": "Click an empty square.", "accent": "blue", "source_url": None,
    },
    {
        "slug": "sorting-lab", "title": "Sorting Lab", "year": "2020", "kind": "project · algorithms",
        "description": "Compare the sorting routines from a sprawling early algorithm visualizer, one operation at a time.",
        "note": "Bubble, selection, insertion, merge, and quicksort are all based on algorithms in the original Python file.",
        "controls": "Pick an algorithm and press Run.", "accent": "green", "source_url": None,
    },
    {
        "slug": "pathfinding-lab", "title": "Pathfinding Lab", "year": "2020–25", "kind": "project · algorithms",
        "description": "Draw walls and watch A*, Dijkstra, breadth-first, depth-first, or greedy search work through them.",
        "note": "This keeps the unusually broad algorithm menu and maze idea from the Pygame/Tkinter visualizer.",
        "controls": "Drag to draw walls, then press Visualize.", "accent": "red", "source_url": None,
    },
]

PROJECTS_BY_SLUG = {project["slug"]: project for project in PROJECTS}


@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS)


@app.route("/play/<slug>")
def play(slug):
    project = PROJECTS_BY_SLUG.get(slug)
    if not project:
        abort(404)
    return render_template("play.html", project=project)


LEGACY_ROUTES = {"Connect4": "connect-four", "Snake": "snake", "SnakeAI": "snake", "Hangman": "hangman", "RubiksCube": "rubiks-cube"}


@app.route("/<project_name>/play")
def legacy_play(project_name):
    slug = LEGACY_ROUTES.get(project_name)
    if not slug:
        abort(404)
    return redirect(url_for("play", slug=slug), code=301)


@app.post("/api/connect-four/new")
def connect_four_new():
    with python_engine_lock:
        state = engine.new_connect_four()
    session["connect_four"] = state
    return jsonify(state)


@app.post("/api/connect-four/move")
def connect_four_move():
    state = session.get("connect_four")
    column = request.get_json(silent=True, force=True).get("column", -1)
    if state is None or not isinstance(column, int) or not 0 <= column < 7:
        abort(400)
    with python_engine_lock:
        state = engine.play_connect_four(state["board"], state["turn"], column)
    session["connect_four"] = state
    return jsonify(state)


@app.post("/api/tic-tac-toe/new")
def tic_tac_toe_new():
    with python_engine_lock:
        state = engine.new_tic_tac_toe()
    session["tic_tac_toe"] = state
    return jsonify(state)


@app.post("/api/tic-tac-toe/move")
def tic_tac_toe_move():
    state = session.get("tic_tac_toe")
    index = request.get_json(silent=True, force=True).get("index", -1)
    if state is None or not isinstance(index, int) or not 0 <= index < 9:
        abort(400)
    with python_engine_lock:
        state = engine.play_tic_tac_toe(state["board"], index)
    session["tic_tac_toe"] = state
    return jsonify(state)


@app.post("/api/rubiks-cube/solve")
def rubiks_cube_solve():
    moves = request.get_json(silent=True, force=True).get("moves", [])
    valid_moves = {"R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'"}
    if not isinstance(moves, list) or len(moves) > 40 or any(move not in valid_moves for move in moves):
        abort(400)
    with python_engine_lock:
        solution = rubiks_cube.solve(moves)
    return jsonify({"solution": solution, "engine": "original-python", "solver": "RubiksCube/main.py:solve3x3"})


@app.post("/api/snake/new")
def snake_new():
    payload = request.get_json(silent=True) or {}
    with python_engine_lock:
        state = snake.new_game(payload.get("ai", False))
    return jsonify(snake.public_state(state))


@app.post("/api/snake/tick")
def snake_tick():
    payload = request.get_json(silent=True) or {}
    state = payload.get("state")
    direction = payload.get("direction")
    positions = state.get("snake") if isinstance(state, dict) else None
    apple = state.get("apple") if isinstance(state, dict) else None
    valid_position = lambda position: (
        isinstance(position, list) and len(position) == 2
        and all(isinstance(value, int) and 0 <= value < 20 for value in position)
    )
    if (
        not isinstance(positions, list) or not 1 <= len(positions) <= 400
        or not all(valid_position(position) for position in positions)
        or not valid_position(apple)
        or state.get("direction") not in {"up", "down", "left", "right"}
        or not isinstance(state.get("ai"), bool)
        or not isinstance(state.get("moves"), int)
        or direction is not None and direction not in {"up", "down", "left", "right"}
    ):
        abort(400)
    state = {
        "snake": positions,
        "apple": apple,
        "direction": state["direction"],
        "ai": state["ai"],
        "over": bool(state.get("over", False)),
        "won": bool(state.get("won", False)),
        "moves": state["moves"],
        "engine": "original-python",
    }
    with python_engine_lock:
        state = snake.tick(state, direction)
    return jsonify(snake.public_state(state))


if __name__ == "__main__":
    app.run(debug=True)
