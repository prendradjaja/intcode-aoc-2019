import inspect


POSITION_MODE = 0
IMMEDIATE_MODE = 1


# mutates the program!
class IntcodeComputer:
    def __init__(self, io=None):
        self.io = io
        self.memory = [99]

    def load_memory(self, memory):
        self.memory = memory

    def run(self):
        memory = self.memory
        ip = 0
        while memory[ip] != 99:
            opcode = get_opcode(memory[ip])
            handler = self.get_handler(opcode)

            params_index = ip + 1
            params_count = self.get_params_count(opcode)
            param_modes = get_param_modes(memory[ip], params_count)
            params = memory[params_index : params_index + params_count]
            params = [Param(p, m) for p, m in zip(params, param_modes)]

            handler(*params)

            ip += params_count + 1
        return memory[0]

    def get_handler(self, opcode):
        return getattr(self, f'handler_{opcode}')

    def get_params_count(self, opcode):
        return len(inspect.signature(self.get_handler(opcode)).parameters)


    ########################
    # INSTRUCTION HANDLERS #
    ########################

    def handler_1(self, in1, in2, out):
        self.memory[out.value] = self.get_value(in1) + self.get_value(in2)

    def handler_2(self, in1, in2, out):
        self.memory[out.value] = self.get_value(in1) * self.get_value(in2)

    def handler_3(self, addr):
        assert self.io is not None
        self.memory[addr.value] = self.io.input()

    def handler_4(self, in1):
        assert self.io is not None
        self.io.output(self.get_value(in1))

    def get_value(self, param):
        if param.mode == POSITION_MODE:
            return self.memory[param.value]
        elif param.mode == IMMEDIATE_MODE:
            return param.value
        else:
            1/0

class Param:
    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

def get_opcode(n):
    return n % 100

def get_param_modes(n, params_count):
    n //= 100
    param_modes = []
    for _ in range(params_count):
        param_modes.append(n % 10)
        n //= 10
    return param_modes
