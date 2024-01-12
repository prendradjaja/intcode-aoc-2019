from puzzle_inputs import day_17_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output, QueueStore


def main():
    computer = IntcodeComputer(
        output = QueueStore()
    )
    computer.run(program)
    text = ''
    for each in computer.output.values:
        text += chr(each)
    image = Image(text.strip().splitlines())

    for line in text.splitlines():
        for ch in line:
            print(ch, end=' ')
        print()

    answer = 0
    for r, row in enumerate(image.data):
        for c, ch in enumerate(row):
            neighbors = list(image.neighbors((r, c)))
            if (
                ch == '#'
                and len(neighbors) == 4
                and all(each == '#' for each in neighbors)
            ):
                alignment_parameter = r * c
                answer += alignment_parameter
    print(answer)


class Image:
    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])

    def in_bounds(self, pos):
        r, c = pos
        return (
            0 <= r < self.height and
            0 <= c < self.width
        )

    def neighbors(self, pos):
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            pos2 = addvec(pos, offset)
            if self.in_bounds(pos2):
                r2, c2 = pos2
                yield self.data[r2][c2]


def addvec(v, w):
    return tuple(a + b for (a, b) in zip(v, w))


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
    main()
