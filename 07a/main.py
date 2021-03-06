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
    last_output = 0
    for setting in phase_settings:
        computer.input = FixedValuesInput([setting, last_output])
        computer.run(program)
        last_output = computer.output.value
    return last_output


if __name__ == '__main__':
    main()
