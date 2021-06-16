from puzzle_inputs import day_5_program as program, day_5b_larger_example
from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

def main():
    """
    >>> main()
    14340395
    """
    computer = IntcodeComputer(
        OneValueInput(5),
        PrintOutput()
    )
    computer.load_memory(program)
    computer.run()

def large_example(n):
    """
    >>> large_example(5)
    999
    >>> large_example(8)
    1000
    >>> large_example(10)
    1001
    """
    computer = IntcodeComputer(
        OneValueInput(n),
        PrintOutput()
    )
    computer.load_memory(day_5b_larger_example)
    computer.run()

if __name__ == '__main__':
    main()
