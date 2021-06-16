from puzzle_inputs import day_9_program as program, day_9a_example_1 as example1
from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput, QueueStore
import itertools


def main():
    print('Answer for part 1:')
    boost(1)

    print('\nAnswer for part 2:')
    boost(2)


def boost(n):
    """
    >>> boost(1)
    3429606717
    """
    # # Skip this test because it's slow and doesn't seem to do anything new
    # >>> boost(2)
    # 33679

    computer = IntcodeComputer(OneValueInput(n), PrintOutput())
    computer.run(program)


def example1_quine():
    """
    >>> example1_quine() == example1
    True
    """
    output = QueueStore()
    computer = IntcodeComputer(None, output)
    computer.run([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99])
    return output.values


if __name__ == '__main__':
    main()
