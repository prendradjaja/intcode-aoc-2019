import inspect

example_input = [1,9,10,3,2,3,11,0,99,30,40,50]
real_input = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,19,10,23,1,23,6,27,1,6,27,31,1,13,31,35,1,13,35,39,1,39,13,43,2,43,9,47,2,6,47,51,1,51,9,55,1,55,9,59,1,59,6,63,1,9,63,67,2,67,10,71,2,71,13,75,1,10,75,79,2,10,79,83,1,83,6,87,2,87,10,91,1,91,6,95,1,95,13,99,1,99,13,103,2,103,9,107,2,107,10,111,1,5,111,115,2,115,9,119,1,5,119,123,1,123,9,127,1,127,2,131,1,5,131,0,99,2,0,14,0]

def handler_1(memory, in1, in2, out):
    memory[out] = memory[in1] + memory[in2]

def handler_2(memory, in1, in2, out):
    memory[out] = memory[in1] * memory[in2]

def get_handler(opcode):
    return globals()[f'handler_{opcode}']

def get_count_args(opcode):
    return len(inspect.signature(get_handler(opcode)).parameters) - 1

# mutates the program!
def execute_program(program):
    memory = program
    ip = 0
    while memory[ip] != 99:
        opcode = memory[ip]
        handler = get_handler(opcode)
        args_index = ip + 1
        args_count = get_count_args(opcode)
        handler(memory, *memory[args_index : args_index + args_count])
        ip += args_count + 1
    print(memory[0])

def set_1202_program_alarm_state(gravity_assist_program):
    gravity_assist_program[1] = 12
    gravity_assist_program[2] = 2

# execute_program(example_input)

set_1202_program_alarm_state(real_input)
execute_program(real_input)
