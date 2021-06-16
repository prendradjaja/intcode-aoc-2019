from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

# n = limit = 4
# i = 1
# total = 0
# while i < limit:
#     total += i
#     i += 1
# print(total)

LOOP = 0
END = 18

# code segment
program = [
    # LOOP: (@8)
    # @103 = i == limit
    8, 100, 101, 103,
    # if @103 jump to END
    1005, 103, END,

    # total += i
    1, 101, 102, 102,
    # i += 1
    101, 1, 101, 101,
    # jump to LOOP
    1105, 1, LOOP,

    # END:
    # print(total)
    4, 102,
    99,
]

# padding and data segment
program += (
    [0] * (100 - len(program)) +
    # n = limit = 4 (@100)
    # i = 1 (@101)
    # total = 0 (@102)
    [4, 1]
)

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
