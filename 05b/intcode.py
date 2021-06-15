import inspect


POSITION_MODE = 0
IMMEDIATE_MODE = 1


class IntcodeComputer:
    def __init__(self, input_=None, output=None):
        self.input = input_
        self.output = output
        self.memory = [99]

    def load_memory(self, memory):
        copy = list(memory)
        self.memory = copy

    def run(self):
        memory = self.memory
        self.ip = 0
        while memory[self.ip] != 99:
            opcode = get_opcode(memory[self.ip])
            handler = self.get_handler(opcode)

            params_index = self.ip + 1
            params_count = self.get_params_count(opcode)
            param_modes = get_param_modes(memory[self.ip], params_count)
            params = memory[params_index : params_index + params_count]
            params = [Param(p, m) for p, m in zip(params, param_modes)]

            ip = handler(*params)

            if ip is None:
                self.ip += params_count + 1
            else:
                self.ip = ip
        return memory[0]

    def get_handler(self, opcode):
        return getattr(self, f'handler_{opcode}')

    def get_params_count(self, opcode):
        return len(inspect.signature(self.get_handler(opcode)).parameters)


    ########################
    # INSTRUCTION HANDLERS #
    ########################

    # add
    def handler_1(self, in1, in2, out):
        self.memory[out.value] = self.get_value(in1) + self.get_value(in2)

    # multiply
    def handler_2(self, in1, in2, out):
        self.memory[out.value] = self.get_value(in1) * self.get_value(in2)

    # input
    def handler_3(self, addr):
        assert self.input is not None
        self.memory[addr.value] = self.input.get_value()

    # output
    def handler_4(self, in1):
        assert self.output is not None
        self.output.put_value(self.get_value(in1))

    # jump-if-true
    def handler_5(self, condition, address):
        if self.get_value(condition) != 0:
            return self.get_value(address)

    # jump-if-false
    def handler_6(self, condition, address):
        if self.get_value(condition) == 0:
            return self.get_value(address)

    # less-than
    def handler_7(self, in1, in2, out):
        self.memory[out.value] = int(self.get_value(in1) < self.get_value(in2))

    # equals
    def handler_8(self, in1, in2, out):
        self.memory[out.value] = int(self.get_value(in1) == self.get_value(in2))

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
