from puzzle_inputs import day_11_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output

import itertools
from collections import defaultdict
from types import SimpleNamespace


WHITE = 'WHITE'
BLACK = 'BLACK'

DIRECTIONS = [
    UP := (-1, 0),
    RIGHT := (0, 1),
    DOWN := (1, 0),
    LEFT := (0, -1),
]

CLOCKWISE = 1
ANTICLOCKWISE = -1


def main():
    # Initialize state
    state = SimpleNamespace(
        panels = defaultdict(lambda: BLACK),
        pos = (0, 0),
        direction = UP,
    )

    # Set up and run computer
    computer = IntcodeComputer(
        input_ = CallbackInput(lambda: int(state.panels[state.pos] == WHITE)),
        output = BivalueCallbackOutput(
            lambda color, turn_direction: handle_outputs(state, color, turn_direction)
        )
    )
    computer.run(program)

    # Count panels
    print(len(state.panels))


class CallbackInput(Input):
    def __init__(self, cb):
        self.cb = cb

    def get_value(self):
        return self.cb()


class BivalueCallbackOutput(Output):
    def __init__(self, cb):
        self.cb = cb
        self.first_value = None

    def put_value(self, value):
        if self.first_value is None:
            self.first_value = value
        else:
            self.cb(self.first_value, value)
            self.first_value = None


def handle_outputs(state, _color, _turn_direction):
    color = {0: BLACK, 1: WHITE}[_color]
    turn_direction = {0: ANTICLOCKWISE, 1: CLOCKWISE}[_turn_direction]

    state.panels[state.pos] = color
    state.direction = turn(state.direction, turn_direction)
    state.pos = addvec(state.pos, state.direction)


def turn(heading, adjustment):
    assert adjustment in [CLOCKWISE, ANTICLOCKWISE]
    idx = (DIRECTIONS.index(heading) + adjustment) % len(DIRECTIONS)
    return DIRECTIONS[idx]


def addvec(v, w):
    return (v[0] + w[0], v[1] + w[1])


if __name__ == '__main__':
    main()
