from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput

# n = limit = 4
# i = 1
# total = 0
# while i < limit:
#     total += i
#     i += 1
# print(total)

LOOP = 8
END = 26

program = [
# n = limit = 4 (@100)
1101, 4, 0, 100,
# i = 1 (@101)
1101, 1, 0, 101,
# total = 0 (@102)
*[],

# LOOP: (@8)
# @103 = i == limit
8, 100, 101, 103,
# if @103 jump to END
1005, 103, 26,

# total += i
1, 101, 102, 102,
# i += 1
101, 1, 101, 101,
# jump to LOOP
1105, 1, 8,

# END:
# print(total)
4, 102,
99,
]

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
