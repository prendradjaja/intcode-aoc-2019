from puzzle_inputs import day_5_program as program
from intcode import IntcodeComputer
from io_devices import ThermalEnvironmentSupervisionTerminalIO

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
    io = ThermalEnvironmentSupervisionTerminalIO()
    computer = IntcodeComputer(io)
    computer.load_memory(program)
    computer.run()

if __name__ == '__main__':
    main()
