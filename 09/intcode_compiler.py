from intcode import IntcodeComputer, Param, POSITION_MODE, IMMEDIATE_MODE, RELATIVE_MODE

class VariableAllocator:
    def __init__(self, code_segment_length, data_segment_length, program):
        self.code_segment_length = code_segment_length
        self.data_segment_length = data_segment_length
        self.program = program  # This will be mutated

        self.nvars = 0

    def make_var(self, initial_value):
        address = self.nvars + self.code_segment_length
        self.program[address] = initial_value
        self.nvars += 1
        return address

def pos(value):
    return Param(value, POSITION_MODE)

def imm(value):
    return Param(value, IMMEDIATE_MODE)

def rel(value):
    return Param(value, RELATIVE_MODE)

def _get_parameter_modes(params):
    result = 0
    for i, param in enumerate(params):
        result += 10**i * param.mode
    return result

for opcode in range(1, 99+1):
    try:
        handler = getattr(IntcodeComputer , f'handler_{opcode}')
    except AttributeError:
        continue

    def _make_instruction_factory(opcode):
        def make_instruction(*params):
            parameter_modes = _get_parameter_modes(params)
            param_values = [p.value for p in params]
            return [100 * parameter_modes + opcode, *param_values]
        return make_instruction

    globals()[handler.name] = _make_instruction_factory(opcode)
