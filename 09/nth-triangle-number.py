from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

# n = limit = 4
# i = 1
# total = 0
# while i < limit:
#     total += i
#     i += 1
# print(total)

CODE_SEGMENT_LENGTH = 100
DATA_SEGMENT_LENGTH = 100

LOOP = 0
END = 18

def make_var(initial_value):
    address = make_var.next
    program[address] = initial_value
    make_var.next += 1
    return address
make_var.next = DATA_SEGMENT_LENGTH

program = [0] * (CODE_SEGMENT_LENGTH + DATA_SEGMENT_LENGTH)

limit    = make_var(4)
i        = make_var(1)
total    = make_var(0)
loopcond = make_var(0)

code = [
    # LOOP: (@8)
    # @103 = i == limit
    8, limit, i, loopcond,
    # if @103 jump to END
    1005, loopcond, END,

    # total += i
    1, i, total, total,
    # i += 1
    101, 1, i, i,
    # jump to LOOP
    1105, 1, LOOP,

    # END:
    # print(total)
    4, total,
    99,
]

program[:len(code)] = code

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
