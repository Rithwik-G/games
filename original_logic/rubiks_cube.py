"""Headless adapter for the original RubiksCube/main.py model and solver.

The original module intertwines its cube mathematics with PyOpenGL drawing.
This loader supplies inert drawing modules so Flask can execute the unchanged
Piece class, face turns, and solve3x3 routine without opening a desktop window.
"""

import importlib.util
import sys
import types
from pathlib import Path


class _Clock:
    def tick(self, *_args):
        return None


def _module(name, **members):
    module = types.ModuleType(name)
    module.__dict__.update(members)
    return module


def _load_original():
    no_op = lambda *_args, **_kwargs: None
    pygame = _module(
        "pygame",
        time=types.SimpleNamespace(Clock=_Clock),
        event=types.SimpleNamespace(get=lambda: []),
        display=types.SimpleNamespace(flip=no_op),
        quit=no_op,
        KEYDOWN=1,
        KEYUP=2,
        QUIT=3,
        MOUSEBUTTONDOWN=4,
        K_LEFT=10,
        K_RIGHT=11,
        K_UP=12,
        K_DOWN=13,
        K_a=14,
        K_d=15,
        K_w=16,
        K_s=17,
    )
    locals_module = _module("pygame.locals", DOUBLEBUF=0, OPENGL=0)
    gl_members = {name: no_op for name in (
        "glBegin", "glColor3fv", "glVertex3fv", "glEnd", "glTranslatef",
        "glEnable", "glClear", "glRotatef",
    )}
    gl_members.update(GL_QUADS=0, GL_DEPTH_TEST=0, GL_COLOR_BUFFER_BIT=0, GL_DEPTH_BUFFER_BIT=0)
    gl = _module("OpenGL.GL", **gl_members)
    glu = _module("OpenGL.GLU", gluPerspective=no_op)
    opengl = _module("OpenGL")
    replacements = {"pygame": pygame, "pygame.locals": locals_module, "OpenGL": opengl, "OpenGL.GL": gl, "OpenGL.GLU": glu}
    previous = {name: sys.modules.get(name) for name in replacements}
    sys.modules.update(replacements)
    try:
        path = Path(__file__).resolve().parents[1] / "RubiksCube" / "main.py"
        spec = importlib.util.spec_from_file_location("rithwik_rubiks_cube", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, old in previous.items():
            if old is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old


original = _load_original()


def create_cube(side_length=3):
    original.BLACK = (0, 0, 0)
    original.YELLOW = (1, 1, 0)
    original.GREEN = (0, 1, 0)
    original.RED = (1, 0, 0)
    original.BLUE = (0, 0, 1)
    original.ORANGE = (1, 0.647, 0)
    original.WHITE = (1, 1, 1)
    original.realChange = 90
    original.solving = False
    original.show = False
    original.HEADLESS = True
    original.moveLstForSolved = []
    cubes = []
    for i in range(side_length ** 2):
        cubes.append(original.Piece(side_length, i))
    for i in range(1, side_length - 1):
        for k in range(i * side_length ** 2, i * side_length ** 2 + side_length):
            cubes.append(original.Piece(side_length, k))
        for k in range(1, side_length - 1):
            cubes.append(original.Piece(side_length, i * side_length ** 2 + k * side_length))
            cubes.append(original.Piece(side_length, i * side_length ** 2 + (k + 1) * side_length - 1))
        for k in range((i + 1) * side_length ** 2 - side_length, (i + 1) * side_length ** 2):
            cubes.append(original.Piece(side_length, k))
    for i in range(side_length ** 2 * (side_length - 1), side_length ** 3):
        cubes.append(original.Piece(side_length, i))
    return cubes


def solve(scramble):
    cubes = create_cube()
    original.basicTurns(cubes, 1, scramble, show=False)
    original.executedMoves = []
    original.solve3x3(cubes, 3, speed=90)
    lookup = {
        ("x", 1, 1): "R", ("x", -1, 1): "R'", ("x", -1, -1): "L", ("x", 1, -1): "L'",
        ("y", 1, 1): "U", ("y", -1, 1): "U'", ("y", -1, -1): "D", ("y", 1, -1): "D'",
        ("z", 1, 1): "F", ("z", -1, 1): "F'", ("z", -1, -1): "B", ("z", 1, -1): "B'",
    }
    return [lookup[(axis, 1 if change > 0 else -1, row)] for axis, change, row in original.executedMoves]
