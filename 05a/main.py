import inspect
from abc import ABC, abstractmethod
from puzzle_inputs import day_5_program as p

POSITION_MODE = 0
IMMEDIATE_MODE = 1

class Param:
    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

class IO(ABC):
    @abstractmethod
    def input(self):
        pass

    @abstractmethod
    def output(self, value):
        pass

class ThermalEnvironmentSupervisionTerminalIO(IO):
    def __init__(self):
        self.input_called = False

    def input(self):
        assert not self.input_called
        self.input_called = True
        return 1

    def output(self, value):
        print(value)

io = ThermalEnvironmentSupervisionTerminalIO()

def handler_1(memory, in1, in2, out):
    memory[out.value] = get_value(memory, in1) + get_value(memory, in2)

def handler_2(memory, in1, in2, out):
    memory[out.value] = get_value(memory, in1) * get_value(memory, in2)

def handler_3(memory, addr):
    memory[addr.value] = io.input()

def handler_4(memory, in1):
    io.output(get_value(memory, in1))

def get_value(memory, param):
    if param.mode == POSITION_MODE:
        return memory[param.value]
    elif param.mode == IMMEDIATE_MODE:
        return param.value

def get_handler(opcode):
    return globals()[f'handler_{opcode}']

def get_count_params(opcode):
    return len(inspect.signature(get_handler(opcode)).parameters) - 1

def get_opcode(n):
    return n % 100

def get_param_modes(n, params_count):
    n //= 100
    param_modes = []
    for _ in range(params_count):
        param_modes.append(n % 10)
        n //= 10
    return param_modes

# mutates the program!
def execute_program(program):
    memory = program
    ip = 0
    while memory[ip] != 99:
        opcode = get_opcode(memory[ip])
        handler = get_handler(opcode)

        params_index = ip + 1
        params_count = get_count_params(opcode)
        param_modes = get_param_modes(memory[ip], params_count)
        params = memory[params_index : params_index + params_count]
        params = [Param(p, m) for p, m in zip(params, param_modes)]

        handler(memory, *params)

        ip += params_count + 1
    return memory[0]

execute_program(p)
