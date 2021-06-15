from puzzle_inputs import day_2_program as program
from intcode import IntcodeComputer

def main():
    """
    >>> main()
    5866714
    """
    computer = IntcodeComputer()
    computer.load_memory(program)
    computer.memory[1] = 12
    computer.memory[2] = 2
    print(computer.run())

if __name__ == '__main__':
    main()
