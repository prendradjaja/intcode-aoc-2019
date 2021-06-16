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

    # total += i  # TODO move this line down after ISMULT3OR5
    1, 101, 102, 102,
    # i += 1
    101, 1, 101, 101,
    # jump to LOOP
    1105, 1, LOOP,

    # ISMULT3OR5: (@120 = temp:ismult3, @121 = temp:ismult5, @122 = result)
    # - checks if i is a multiple of 3 or 5
    # TODO

    # ISMULT: (@110 = factor, @111 = output address, @112 = temp, @113 = return ip)
    # - checks if i is a multiple of factor
    # temp = 0
    # while temp < i:
    #     temp += factor
    # @111 = temp == i
    # jump to @113

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
