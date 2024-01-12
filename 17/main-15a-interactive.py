import curses
from types import SimpleNamespace
import time
from copy import copy
import random

from puzzle_inputs import day_15_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output


def main(_stdscr):
    global HEIGHT, HALF_WIDTH, stdscr, last_movement_command, droid_position
    stdscr = _stdscr

    HEIGHT = curses.LINES
    HALF_WIDTH = curses.COLS // 2

    last_movement_command = None
    droid_position = SimpleNamespace(r=0, c=0)

    stdscr.clear()
    draw(droid_position, 'D')

    computer = IntcodeComputer(
        input_ = CallbackInput(handle_input),
        output = CallbackOutput(handle_output),
    )
    computer.run(program)


def handle_input():
    global last_movement_command

    while True:
        key = stdscr.getkey()
        if key == 'KEY_UP':
            result = 1
            break
        elif key == 'KEY_DOWN':
            result = 2
            break
        elif key == 'KEY_LEFT':
            result = 3
            break
        elif key == 'KEY_RIGHT':
            result = 4
            break

    last_movement_command = result
    return result


def handle_output(output):
    if output == 0:
        wall_position = get_movement_destination(last_movement_command, droid_position)
        draw(wall_position, '#')
    elif output in [1, 2]:
        previous_position = copy(droid_position)
        move_droid(last_movement_command, droid_position)
        draw(previous_position, '.')
        draw(droid_position, 'D')
        if output == 2:
            stdscr.addstr(1, 0, f'Oxygen system found! Location: {droid_position}')
            draw(SimpleNamespace(r=0, c=0), 'S')
            draw(droid_position, 'E')
            stdscr.getkey()
    else:
        raise Exception('Unexpected output')


def draw(position, ch):
    stdscr.addstr(
        position.r + HEIGHT // 2,
        (position.c * 2) + HALF_WIDTH,
        ch
    )
    stdscr.addstr(0, 0, '')  # Keep the cursor in the corner
    stdscr.refresh()


def get_movement_destination(direction, position):
    new_position = copy(position)
    if direction == 1:
        new_position.r -= 1
    elif direction == 2:
        new_position.r += 1
    elif direction == 3:
        new_position.c -= 1
    elif direction == 4:
        new_position.c += 1
    else:
        raise Exception('Invalid direction')
    return new_position


def move_droid(direction, droid_position):
    destination = get_movement_destination(direction, droid_position)
    droid_position.r = destination.r
    droid_position.c = destination.c


class CallbackInput(Input):
    def __init__(self, cb):
        self.cb = cb

    def get_value(self):
        return self.cb()


class CallbackOutput(Output):
    def __init__(self, cb):
        self.cb = cb

    def put_value(self, value):
        self.cb(value)


if __name__ == '__main__':
    curses.wrapper(main)
