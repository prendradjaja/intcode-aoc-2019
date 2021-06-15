from puzzle_inputs import day_2_program as program, day_2_target_output as target_output
from intcode import IntcodeComputer

def main():
    """
    >>> main()
    5208
    """
    computer = IntcodeComputer()

    for in1 in range(0, 99+1):
        for in2 in range(0, 99+1):
            copy = list(program)
            computer.load_memory(copy)
            computer.memory[1] = in1
            computer.memory[2] = in2
            output = computer.run()
            if output == target_output:
                print(100 * in1 + in2)
                return

if __name__ == '__main__':
    main()
