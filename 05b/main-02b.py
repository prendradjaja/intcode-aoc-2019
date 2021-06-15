from puzzle_inputs import day_2_program as program, day_2_target_output as target_output
from intcode import IntcodeComputer

def main(
    in1s = range(0, 99+1),
    in2s = range(0, 99+1)
):
    """
    >>> main([52], [8])  # Don't run on all inputs when testing -- faster to just provide the known answer
    5208
    """
    computer = IntcodeComputer()

    for in1 in in1s:
        for in2 in in2s:
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
