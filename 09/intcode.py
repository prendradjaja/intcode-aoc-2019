import inspect

from memory import Memory


POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


class IntcodeComputer:
    def __init__(self, input_=None, output=None):
        self.input = input_
        self.output = output
        self.memory = Memory()
        self.memory.load([99])

    def load_memory(self, program):
        self.memory.load(program)

    def run(self, program=None):
        if program:
            self.load_memory(program)
        self.ip = 0
        self.relative_base = 0
        last_opcode = None
        while last_opcode != 99:
            last_opcode = self.step()
        return last_opcode

    # Returns None if continue
    def step(self):
        memory = self.memory
        opcode = get_opcode(memory[self.ip])
        handler = self.get_handler(opcode)

        params_index = self.ip + 1
        params_count = self.get_params_count(opcode)
        param_modes = get_param_modes(memory[self.ip], params_count)
        params = memory[params_index : params_index + params_count]
        params = [Param(p, m) for p, m in zip(params, param_modes)]

        ip = handler(*params)

        # print(self.get_handler(opcode).name, self.ip, self.memory[100:105], sep='\t')
        # if ip:
        #     print()

        if ip is None:
            self.ip += params_count + 1
        else:
            self.ip = ip
        return opcode

    def get_handler(self, opcode):
        return getattr(self, f'handler_{opcode}')

    def get_params_count(self, opcode):
        return len(inspect.signature(self.get_handler(opcode)).parameters)

    def get_value(self, param):
        if param.mode == POSITION_MODE:
            return self.memory[param.value]
        elif param.mode == IMMEDIATE_MODE:
            return param.value
        elif param.mode == RELATIVE_MODE:
            return self.memory[self.relative_base + param.value]
        else:
            1/0

    def set_value(self, address, value):
        if address.mode == POSITION_MODE:
            self.memory[address.value] = value
        elif address.mode == RELATIVE_MODE:
            self.memory[self.relative_base + address.value] = value
        else: # Immediate mode is not allowed for "set" instructions
            1/0


    ########################
    # INSTRUCTION HANDLERS #
    ########################

    # add
    def handler_1(self, in1, in2, out):
        self.set_value(out, self.get_value(in1) + self.get_value(in2))
    handler_1.name = 'add'

    # multiply
    def handler_2(self, in1, in2, out):
        self.set_value(out, self.get_value(in1) * self.get_value(in2))
    handler_2.name = 'mul'

    # input
    def handler_3(self, addr):
        assert self.input is not None
        self.set_value(addr, self.input.get_value())
    handler_3.name = 'inp'

    # output
    def handler_4(self, in1):
        assert self.output is not None
        self.output.put_value(self.get_value(in1))
    handler_4.name = 'out'

    # jump-if-true
    def handler_5(self, condition, address):
        if self.get_value(condition) != 0:
            return self.get_value(address)
    handler_5.name = 'jnz'

    # jump-if-false
    def handler_6(self, condition, address):
        if self.get_value(condition) == 0:
            return self.get_value(address)
    handler_6.name = 'jz'

    # less-than
    def handler_7(self, in1, in2, out):
        self.set_value(out, int(self.get_value(in1) < self.get_value(in2)))
    handler_7.name = 'lt'

    # equals
    def handler_8(self, in1, in2, out):
        self.set_value(out, int(self.get_value(in1) == self.get_value(in2)))
    handler_8.name = 'eq'

    # adjust relative base
    def handler_9(self, in1):
        self.relative_base += self.get_value(in1)
    handler_9.name = 'adjrel'

    # stop
    def handler_99(self):
        pass
    handler_99.name = 'halt'


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
