import inspect
from io_devices import ThermalEnvironmentSupervisionTerminalIO


POSITION_MODE = 0
IMMEDIATE_MODE = 1


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


class Param:
    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

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
