import curses
from types import SimpleNamespace
import time

from puzzle_inputs import day_13_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output


def main(stdscr):
    stdscr.clear()
    stdscr.nodelay(True)

    positions = SimpleNamespace(ball=0, paddle=0)
    computer = IntcodeComputer(
        input_ = CallbackInput(lambda: handle_input(stdscr, positions)),
        output = TrivalueCallbackOutput(lambda outputs: handle_outputs(stdscr, outputs, positions)),
    )
    computer.load_memory(program)
    computer.memory[0] = 2
    computer.run()


class CallbackInput(Input):
    def __init__(self, cb):
        self.cb = cb

    def get_value(self):
        return self.cb()


class TrivalueCallbackOutput(Output):
    def __init__(self, cb):
        self.cb = cb
        self.values = []

    def put_value(self, value):
        if len(self.values) < 2:
            self.values.append(value)
        else:
            self.cb(self.values + [value])
            self.values = []


def handle_input(stdscr, positions):
    time.sleep(0.1)
    stdscr.refresh()
    try:
        key = stdscr.getkey()
    except curses.error:
        key = None
    if key == 'KEY_LEFT':
        return -1
    elif key == 'KEY_RIGHT':
        return 1
    else:
        return 0


def handle_outputs(stdscr, outputs, positions):
    x, y, tile_id = outputs
    if (x, y) == (-1, 0):
        stdscr.addstr(0, 0, f'Score: {tile_id}')
    else:
        stdscr.addstr(y + 2, x * 2, str(tile_id or '.'))
        if tile_id == 4:
            positions.ball = x
        elif tile_id == 3:
            positions.paddle = x


def signum(n):
    if n > 0:
        return 1
    elif n < 0:
        return -1
    else:
        return 0


if __name__ == '__main__':
    curses.wrapper(main)
