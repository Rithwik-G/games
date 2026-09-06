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
        "description": "A Connect Four opponent powered by alpha-beta minimax, with a quick browser board and rematches.",
        "note": "The computer prefers the center columns and searches ahead with alpha-beta pruning.",
        "controls": "Click a column to drop a piece.", "accent": "red",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/Connect4",
    },
    {
        "slug": "snake", "title": "Snake / Snake AI", "year": "2021", "kind": "game · hamiltonian path",
        "description": "Play the 20×20 Snake board yourself, or let the Hamiltonian-cycle AI patiently fill it.",
        "note": "A Python backend handles the 20×20 grid, movement, apples, and Hamiltonian shortcut logic.",
        "controls": "Arrow keys or WASD. Space pauses; R restarts.", "accent": "green",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/SnakeAI",
    },
    {
        "slug": "hangman", "title": "Hangman", "year": "2020", "kind": "game · two player",
        "description": "One person enters a secret phrase, then hands the screen over for a local two-player round.",
        "note": "Nine misses, a pass-the-keyboard setup, and a clean new-round loop.",
        "controls": "Type or click letters. R starts a new round.", "accent": "ink",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/Hangman",
    },
    {
        "slug": "rubiks-cube", "title": "Rubik’s Cube", "year": "2021", "kind": "project · cube solver",
        "description": "A compact cube workbench for turning, scrambling, and replaying a solution in the browser.",
        "note": "A 2,000-line Piece model and solve3x3 routine run in Python, paired with an interactive canvas-rendered 3D view.",
        "controls": "Use the face buttons; hold Shift for counter-clockwise turns.", "accent": "blue",
        "source_url": "https://github.com/Rithwik-G/games/tree/main/RubiksCube",
    },
    {
        "slug": "space-invaders", "title": "Space Invaders", "year": "2021", "kind": "game · arcade",
        "description": "A six-enemy arcade loop with movement, collision, firing, scoring, and respawns.",
        "note": "Includes keyboard and touch controls, pause, and a clean restart.",
        "controls": "Left/right or A/D to move. Space fires.", "accent": "violet", "source_url": None,
    },
    {
        "slug": "tic-tac-toe", "title": "Tic-Tac-Toe", "year": "2020", "kind": "game · minimax",
        "description": "A tiny, stubborn opponent powered by alpha-beta minimax.",
        "note": "You are O, the computer is X, and the computer opens.",
        "controls": "Click an empty square.", "accent": "blue", "source_url": None,
    },
    {
        "slug": "sorting-lab", "title": "Sorting Lab", "year": "2020", "kind": "project · algorithms",
        "description": "Compare five sorting routines one operation at a time.",
        "note": "Bubble, selection, insertion, merge, and quicksort share one visual workspace.",
        "controls": "Pick an algorithm and press Run.", "accent": "green", "source_url": None,
    },
    {
        "slug": "pathfinding-lab", "title": "Pathfinding Lab", "year": "2020–25", "kind": "project · algorithms",
        "description": "Draw walls and watch A*, Dijkstra, breadth-first, depth-first, or greedy search work through them.",
        "note": "Includes five search strategies, editable walls, and a maze generator.",
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
    return jsonify({"solution": solution, "engine": "python", "solver": "solve3x3"})


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
        "engine": "python",
    }
    with python_engine_lock:
        state = snake.tick(state, direction)
    return jsonify(snake.public_state(state))


if __name__ == "__main__":
    app.run(debug=True)
