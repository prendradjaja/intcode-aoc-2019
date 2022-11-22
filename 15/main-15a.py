'''
Explores the maze via random walk. With enough luck and/or patience :), the droid will eventually
find the oxygen system!

TODO Write code to find the shortest path. Currently, the program simply pauses after finding the
oxygen system, displaying the start position (S) and oxygen system (E); and allowing the user to
manually count the number of steps in the shortest path. (See 15a.txt)
'''

import curses
from types import SimpleNamespace
import time
from copy import copy
import random

from puzzle_inputs import day_15_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output


def main(_stdscr):
    global HEIGHT, HALF_WIDTH, stdscr, last_movement_command, droid_position, maze_map
    stdscr = _stdscr

    HEIGHT = curses.LINES
    HALF_WIDTH = curses.COLS // 2

    last_movement_command = None
    droid_position = SimpleNamespace(r=0, c=0)
    maze_map = {(0, 0): '.'}

    stdscr.clear()
    draw(droid_position, 'D')
    draw2(SimpleNamespace(r=0, c=0))

    computer = IntcodeComputer(
        input_ = CallbackInput(handle_input),
        output = CallbackOutput(handle_output),
    )
    computer.run(program)


def handle_input():
    global last_movement_command
    # stdscr.getkey()
    last_movement_command = random.randint(1, 4)
    return last_movement_command


# def handle_input():
#     global last_movement_command
#     while True:
#         key = stdscr.getkey()
#         if key == 'KEY_UP':
#             result = 1
#             break
#         elif key == 'KEY_DOWN':
#             result = 2
#             break
#         elif key == 'KEY_LEFT':
#             result = 3
#             break
#         elif key == 'KEY_RIGHT':
#             result = 4
#             break
#     last_movement_command = result
#     return result


def handle_output(output):
    if output == 0:
        wall_position = get_movement_destination(last_movement_command, droid_position)
        draw(wall_position, '#')
        maze_map[to_tuple(wall_position)] = '#'
        draw2(wall_position)
        check_neighbors(wall_position)
    elif output in [1, 2]:
        previous_position = copy(droid_position)
        move_droid(last_movement_command, droid_position)
        draw(previous_position, '.')
        draw(droid_position, 'D')
        if to_tuple(droid_position) not in maze_map:
            maze_map[to_tuple(droid_position)] = '.'
            draw2(droid_position)
        check_neighbors(droid_position)
        if output == 2:
            stdscr.addstr(1, 0, f'Oxygen system found! Location: {droid_position}')
            draw(SimpleNamespace(r=0, c=0), 'S')
            draw(droid_position, 'E')
            stdscr.getkey()
    else:
        raise Exception('Unexpected output')


def check_neighbors(position):
    check(get_movement_destination(1, position))
    check(get_movement_destination(2, position))
    check(get_movement_destination(3, position))
    check(get_movement_destination(4, position))


def check(position):
    neighbors = [
        get_movement_destination(1, position),
        get_movement_destination(2, position),
        get_movement_destination(3, position),
        get_movement_destination(4, position),
    ]
    if maze_map.get(to_tuple(position), None) == '.' and all(to_tuple(neighbor) in maze_map for neighbor in neighbors):
        maze_map[to_tuple(position)] = 'o'
        draw2(position)


MAX_LINES = 20
class Logger:
    def __init__(self):
        self.lines = ['' * 100] * MAX_LINES

    def log(self, line=''):
        line = str(line)[:100].ljust(100)
        self.lines.pop(0)
        self.lines.append(line)
        for i, line in enumerate(reversed(['---'] + self.lines)):
            stdscr.addstr(HEIGHT - i - 1, 0, line)
        stdscr.addstr(0, 0, '')  # Keep the cursor in the corner

log = Logger().log



def to_tuple(position):
    return (position.r, position.c)


def draw(position, ch):
    stdscr.addstr(
        position.r + HEIGHT // 2,
        (position.c * 2) + HALF_WIDTH // 2,
        ch
    )
    stdscr.addstr(0, 0, '')  # Keep the cursor in the corner
    stdscr.refresh()


def draw2(position):
    ch = maze_map[to_tuple(position)]
    stdscr.addstr(
        position.r + HEIGHT // 2,
        (position.c * 2) + (3 * HALF_WIDTH // 2),
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
