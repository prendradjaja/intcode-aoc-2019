from intcode import IntcodeComputer
from io_devices import OneValueInput, PrintOutput
from intcode_compiler import *

CODE_SEGMENT_LENGTH = 100
DATA_SEGMENT_LENGTH = 100
'';                                                                                                 program = [0] * (CODE_SEGMENT_LENGTH + DATA_SEGMENT_LENGTH); va = VariableAllocator(CODE_SEGMENT_LENGTH, DATA_SEGMENT_LENGTH, program)

limit               = va.make_var(10)
i                   = va.make_var(1)
total               = va.make_var(0)
loopcond            = va.make_var()

ismult3 = va.make_var()

ismult_factor = va.make_var()
ismult_result = va.make_var()
ismult_temp = va.make_var()
ismult_loopcond = va.make_var()
ismult_continue = va.make_var()

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

# ];ISMULT                                                                                            = len(code); code += [
#     *add(imm(0), imm(0), pos(ismult_temp)),
# ];ISMULT_LOOP                                                                                       = len(code); code += [
#     *lt(pos(ismult_temp), pos(i), pos(ismult_loopcond)),
#     *jnz(pos(ismult_loopcond), imm(lambda: ISMULT_END)),
#     *add(pos(ismult_factor), pos(ismult_temp), pos(ismult_temp)),
# ];ISMULT_END                                                                                        = len(code); code += [
#     *eq(),
];                                                                                                  code = [n if isinstance(n, int) else n() for n in code]; assert len(code) <= CODE_SEGMENT_LENGTH; program[:len(code)] = code

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
