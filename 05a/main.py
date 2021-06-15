from puzzle_inputs import day_5_program as program
from intcode import IntcodeComputer
from io_devices import ThermalEnvironmentSupervisionTerminalIO

io = ThermalEnvironmentSupervisionTerminalIO()

computer = IntcodeComputer(io)
computer.load_memory(program)
computer.run()
