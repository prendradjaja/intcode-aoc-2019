from puzzle_inputs import day_5_program as program, day_5b_larger_example
from intcode import IntcodeComputer
from io_devices import OneInputAndPrintIO

def main():
    """
    >>> main()
    14340395
    """
    io = OneInputAndPrintIO(5)
    computer = IntcodeComputer(io)
    computer.load_memory(program)
    computer.run()

def large_example():
    """
    >>> large_example()
    """

if __name__ == '__main__':
    main()
