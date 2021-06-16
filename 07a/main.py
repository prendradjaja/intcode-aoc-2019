from puzzle_inputs import day_7_program as program
from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

def main():
    """
    >>> main()
    """
    computer = IntcodeComputer()
    computer.load_memory(program)
    computer.run()

if __name__ == '__main__':
    main()
