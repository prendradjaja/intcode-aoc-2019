from puzzle_inputs import day_13_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output


def main():
    canvas = {}
    computer = IntcodeComputer(
        output = TrivalueCallbackOutput(lambda outputs: handle_outputs(canvas, outputs))
    )
    computer.run(program)

    answer = sum(tile_id == 2 for pos, tile_id in canvas.items())
    print('Answer:', answer)

    xmin = min(x for (x, y) in canvas)
    xmax = max(x for (x, y) in canvas)
    ymin = min(y for (x, y) in canvas)
    ymax = max(y for (x, y) in canvas)
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            pixel = canvas.get((x, y), '.') or '.'
            print(pixel, end=' ')
        print()


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


def handle_outputs(canvas, outputs):
    x, y, tile_id = outputs
    canvas[x, y] = tile_id


if __name__ == '__main__':
    main()
