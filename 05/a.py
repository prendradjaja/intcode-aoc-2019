import inspect

# example_input = [1,9,10,3,2,3,11,0,99,30,40,50]
# real_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,19,10,23,1,23,6,27,1,6,27,31,1,13,31,35,1,13,35,39,1,39,13,43,2,43,9,47,2,6,47,51,1,51,9,55,1,55,9,59,1,59,6,63,1,9,63,67,2,67,10,71,2,71,13,75,1,10,75,79,2,10,79,83,1,83,6,87,2,87,10,91,1,91,6,95,1,95,13,99,1,99,13,103,2,103,9,107,2,107,10,111,1,5,111,115,2,115,9,119,1,5,119,123,1,123,9,127,1,127,2,131,1,5,131,0,99,2,0,14,0]
#
# target_output = 19690720

POSITION_MODE = 0
IMMEDIATE_MODE = 1

class Param:
    def __init__(self, value, mode):
        self.value = value
        self.mode = mode

def handler_1(memory, in1, in2, out):
    memory[out.value] = get_value(memory, in1) + get_value(memory, in2)

def handler_2(memory, in1, in2, out):
    memory[out.value] = get_value(memory, in1) * get_value(memory, in2)

def get_value(memory, param):
    if param.mode == POSITION_MODE:
        return memory[param.value]
    elif param.mode == IMMEDIATE_MODE:
        return param.valu

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

# for in1 in range(0, 99+1):
#     for in2 in range(0, 99+1):
#         gravity_assist_program = list(real_input)
#         gravity_assist_program[1] = in1
#         gravity_assist_program[2] = in2
#         output = execute_program(gravity_assist_program)
#         if output == target_output:
#             print(100 * in1 + in2)
#             exit()
