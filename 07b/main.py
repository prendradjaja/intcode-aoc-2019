from puzzle_inputs import day_7_program as program
from intcode import IntcodeComputer
from io_devices import OneValueStore, QueueStore
import itertools


all_phase_settings = [5, 6, 7, 8, 9]
all_phase_settings = range(5)

def main():
    """
    """
    program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    print(get_thruster_signal([9,8,7,6,5], program))

    return
    print(max(
        get_thruster_signal(phase_settings, program)
        for phase_settings in itertools.permutations(all_phase_settings)
    ))


def get_thruster_signal(phase_settings, program):
    """
    >>> get_thruster_signal([2, 3, 0, 4, 1], program)
    24405
    """
    count_amplifiers = len(phase_settings)

    # Create computers and connect them to each other
    computers = []
    last_output = QueueStore()
    for i in range(count_amplifiers):
        computer = IntcodeComputer()
        computers.append(computer)
        computer.input = last_output
        computer.output = QueueStore()
        last_output = computer.output
    computers[-1].output = computers[0].input

    # Load programs and initial values
    for computer, phase_setting in zip(computers, phase_settings):
        computer.input.put_value(phase_setting)
        computer.ip = 0
        computer.load_memory(program)
    computers[0].input.put_value(0)

    stopped = [False] * count_amplifiers

    for i in itertools.cycle(range(count_amplifiers)):
        if all(stopped):
            break

        computer = computers[i]
        last_opcode = None
        while last_opcode != 4 and last_opcode != 99:
            last_opcode = computer.step()
            print('   ' * i, last_opcode)
        if last_opcode == 99:
            stopped[i] = True

    return computers[-1].output.get_value()


if __name__ == '__main__':
    main()
