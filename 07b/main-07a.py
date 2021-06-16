from puzzle_inputs import day_7_program as program, day_7a_last_example
from intcode import IntcodeComputer
from io_devices import FixedValuesInput, OneValueStore
import itertools


def main(program=program):
    """
    >>> main()
    24405
    >>> main(day_7a_last_example)
    65210
    """
    computer = IntcodeComputer()
    computer.output = OneValueStore()
    print(max(
        get_thruster_signal(phase_settings, computer, program)
        for phase_settings in itertools.permutations(range(5))
    ))


def get_thruster_signal(phase_settings, computer, program):
    """
    >>> get_thruster_signal([2, 3, 0, 4, 1], IntcodeComputer(None, OneValueStore()), program)
    24405
    """
    last_output = 0
    for i, setting in enumerate(phase_settings):
        print('prog', i)
        computer.input = FixedValuesInput([setting, last_output])
        computer.load_memory(program)
        computer.ip = 0
        last_opcode = None
        while last_opcode != 99:
            last_opcode = computer.step()
            print(last_opcode)
        last_output = computer.output.value
        print()
    return last_output


if __name__ == '__main__':
    print(get_thruster_signal([2, 3, 0, 4, 1], IntcodeComputer(None, OneValueStore()), program))
    # main()
