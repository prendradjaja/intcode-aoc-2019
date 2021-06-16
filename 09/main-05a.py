from puzzle_inputs import day_5_program as program
from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

def main():
    """
    >>> main()
    0
    0
    0
    0
    0
    0
    0
    0
    0
    7692125
    """
    computer = IntcodeComputer(
        OneValueInput(1),
        PrintOutput()
    )
    computer.load_memory(program)
    computer.run()

if __name__ == '__main__':
    main()
