from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput
from intcode_compiler import *

# # Maybe use this: replace `lambda: SOME_LABEL` with `L.SOME_LABEL`
# class L:
#     def __getattr__(self, name):
#         return lambda: globals()[name]
# L = L()

CODE_SEGMENT_LENGTH = 100
DATA_SEGMENT_LENGTH = 100
'';                                                                                                 program = [0] * (CODE_SEGMENT_LENGTH + DATA_SEGMENT_LENGTH); va = VariableAllocator(CODE_SEGMENT_LENGTH, DATA_SEGMENT_LENGTH, program)

limit               = va.make_var(4)
i                   = va.make_var(1)
total               = va.make_var(0)
loopcond            = va.make_var(0)

# n = limit = 4
# i = 1
# total = 0
# while i < limit:
#     total += i
#     i += 1
# print(total)

# code = [
# ];LOOP                                                                                              = len(code); code += [
#     # loopcond = i == limit
#     8, limit, i, loopcond,
#     # if loopcond jump to END
#     1005, loopcond, lambda: END,
#
#     # total += i
#     1, i, total, total,
#     # i += 1
#     101, 1, i, i,
#     # jump to LOOP
#     1105, 1, lambda: LOOP,
# ];END                                                                                               = len(code); code += [
#     # print total
#     4, total,
#     99,
# ];                                                                                                  code = [n if isinstance(n, int) else n() for n in code]; assert len(code) <= CODE_SEGMENT_LENGTH; program[:len(code)] = code

code = [
];LOOP                                                                                              = len(code); code += [
    *eq(pos(limit), pos(i), pos(loopcond)),
    *jnz(pos(loopcond), imm(lambda: END)),
    *add(pos(i), pos(total), pos(total)),
    *add(imm(1), pos(i), pos(i)),
    *jnz(imm(1), imm(lambda: LOOP)),
];END                                                                                               = len(code); code += [
    *out(pos(total)),
    *halt(),
];                                                                                                  code = [n if isinstance(n, int) else n() for n in code]; assert len(code) <= CODE_SEGMENT_LENGTH; program[:len(code)] = code

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
