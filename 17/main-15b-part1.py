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
    global HEIGHT, HALF_WIDTH, stdscr, last_movement_command, droid_position, maze_map, oxygen_system_position
    stdscr = _stdscr

    # random.seed(3)

    HEIGHT = curses.LINES
    HALF_WIDTH = curses.COLS // 2

    last_movement_command = None
    droid_position = (0, 0)
    maze_map = {(0, 0): '.'}

    stdscr.clear()
    draw(droid_position, 'D')
    draw2( (0, 0) )

    computer = IntcodeComputer(
        input_ = CallbackInput(handle_input),
        output = CallbackOutput(handle_output),
    )
    computer.run(program)


def towards_nearest_dot():
    def get_neighbors(node):
        result = []
        for direction in [1, 2, 3, 4]:
            neighbor = get_movement_destination(direction, node)
            if maze_map.get(neighbor, None) in ['.', 'o']:
                result.append(neighbor)
        return result

    def bfs():
        node = droid_position
        visited = {node}
        parents = {}
        q = [node]
        while q:
            node = q.pop(0)
            # log(str(node))
            for v in get_neighbors(node):
                if v not in visited:
                    parents[v] = node
                    if maze_map.get(v, None) == '.':
                        return v, parents
                    visited.add(v)
                    q.append(v)
        # raise Exception('No dot found')
        draw(oxygen_system_position, 'E')
        stdscr.addstr(0, 0, 'Done')
        stdscr.getkey()

    assert maze_map.get(droid_position, None) != '.'
    result = bfs()
    # stdscr.getkey()
    destination, parents = result

    path = []
    node = destination
    while node != droid_position:
        path.append(node)
        node = parents[node]
    next_position = path[-1]
    direction = positions_to_direction(droid_position, next_position)

    return direction

    # stdscr.addstr(0, 0, f'{destination} {path} {direction}')
    # stdscr.refresh()


def positions_to_direction(pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    if r2 == r1 - 1:
        assert c1 == c2
        return 1
    elif r2 == r1 + 1:
        assert c1 == c2
        return 2
    elif c2 == c1 - 1:
        assert r1 == r2
        return 3
    elif c2 == c1 + 1:
        assert r1 == r2
        return 4
    raise Exception('Invalid params to positions_to_direction()')



def handle_input():
    global last_movement_command

    # if random.random() < 0.001:
    #     get_nearest_dot()
    #     stdscr.getkey()

    # stdscr.getkey()

    if maze_map[droid_position] == '.':
        # for direction in [1, 2, 3, 4]:
        #     neighbor = get_movement_destination(direction, droid_position)
        #     if neighbor not in maze_map:
        #         result = direction
        #         break
        result = random.randint(1, 4)
    else:
        result = towards_nearest_dot()
        # log(result)
        # stdscr.getkey()


    last_movement_command = result
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
    global oxygen_system_position
    if output == 0:
        wall_position = get_movement_destination(last_movement_command, droid_position)
        draw(wall_position, '#')
        maze_map[wall_position] = '#'
        draw2(wall_position)
        check_neighbors(wall_position)
    elif output in [1, 2]:
        previous_position = droid_position
        move_droid(last_movement_command, droid_position)
        draw(previous_position, '.')
        draw(droid_position, 'D')
        if droid_position not in maze_map:
            maze_map[droid_position] = '.'
            draw2(droid_position)
        check_neighbors(droid_position)
        if output == 2:
            stdscr.addstr(1, 0, f'Oxygen system found! Location: {droid_position}')
            draw((0, 0), 'S')
            oxygen_system_position = droid_position
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
    if maze_map.get(position, None) == '.' and all(neighbor in maze_map for neighbor in neighbors):
        maze_map[position] = 'o'
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



def draw(position, ch):
    r, c = position
    stdscr.addstr(
        r + HEIGHT // 2,
        # (c * 2) + HALF_WIDTH // 2,
        c + HALF_WIDTH // 2,
        ch
    )
    stdscr.addstr(0, 0, '')  # Keep the cursor in the corner
    stdscr.refresh()


def draw2(position):
    return
    ch = maze_map[position]
    r, c = position
    stdscr.addstr(
        r + HEIGHT // 2,
        (c * 2) + (3 * HALF_WIDTH // 2),
        ch
    )
    stdscr.addstr(0, 0, '')  # Keep the cursor in the corner
    stdscr.refresh()


def get_movement_destination(direction, position):
    r, c = position
    if direction == 1:
        return (r - 1, c)
    elif direction == 2:
        return (r + 1, c)
    elif direction == 3:
        return (r, c - 1)
    elif direction == 4:
        return (r, c + 1)
    else:
        raise Exception('Invalid direction')
    return new_position


def move_droid(direction, _droid_position):
    global droid_position
    droid_position = get_movement_destination(direction, _droid_position)


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
