import inspect
from abc import ABC, abstractmethod

p = [3,225,1,225,6,6,1100,1,238,225,104,0,1002,114,46,224,1001,224,-736,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1,166,195,224,1001,224,-137,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,1001,169,83,224,1001,224,-90,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,101,44,117,224,101,-131,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1101,80,17,225,1101,56,51,225,1101,78,89,225,1102,48,16,225,1101,87,78,225,1102,34,33,224,101,-1122,224,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,66,53,224,101,-119,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,1102,51,49,225,1101,7,15,225,2,110,106,224,1001,224,-4539,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,88,78,225,102,78,101,224,101,-6240,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,226,677,224,102,2,223,223,1006,224,329,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,344,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,1007,226,677,224,1002,223,2,223,1005,224,374,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,389,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,404,1001,223,1,223,1007,226,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,1107,677,226,224,1002,223,2,223,1006,224,434,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,449,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,464,1001,223,1,223,108,226,226,224,1002,223,2,223,1006,224,479,1001,223,1,223,1008,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,509,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,524,101,1,223,223,7,226,677,224,1002,223,2,223,1006,224,539,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,554,1001,223,1,223,7,226,226,224,1002,223,2,223,1006,224,569,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,584,101,1,223,223,1108,677,677,224,102,2,223,223,1006,224,599,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,8,677,677,224,1002,223,2,223,1006,224,629,1001,223,1,223,107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

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
