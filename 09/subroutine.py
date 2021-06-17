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

x = va.make_var()
y = va.make_var()
z = va.make_var()

a = va.make_var()
b = va.make_var()
c = va.make_var()

arg1 = va.make_var()
arg2 = va.make_var()
result = va.make_var()
continue_at = va.make_var()

# x = 1
# y = 2
# z = add(x, y)

# a = 4
# b = 5
# c = add(a, b)

code = [
];START                                                                                             = len(code); code += [
    *add(imm(1), imm(0), pos(x)),
    *add(imm(2), imm(0), pos(y)),

        *add(pos(x), imm(0), pos(arg1)),
        *add(pos(y), imm(0), pos(arg2)),
        *add(imm(lambda:Z), imm(0), pos(continue_at)),
    *jnz(imm(1), imm(lambda:SUBROUTINE)), # subroutine -- indented lines are pre- and post- subroutine
];Z                                                                                                 = len(code); code += [
        *add(pos(result), imm(0), pos(z)),

    *add(imm(4), imm(0), pos(a)),
    *add(imm(5), imm(0), pos(b)),

        *add(pos(a), imm(0), pos(arg1)),
        *add(pos(b), imm(0), pos(arg2)),
        *add(imm(lambda:C), imm(0), pos(continue_at)),
    *jnz(imm(1), imm(lambda:SUBROUTINE)),
];C                                                                                                 = len(code); code += [
        *add(pos(result), imm(0), pos(c)),

    *out(pos(x)),
    *out(pos(y)),
    *out(pos(z)),
    *out(pos(a)),
    *out(pos(b)),
    *out(pos(c)),

    *halt(),

];SUBROUTINE                                                                                        = len(code); code += [
    *add(pos(arg1), pos(arg2), pos(result)),
    *jnz(imm(1), pos(continue_at)),
];                                                                                                  code = [n if isinstance(n, int) else n() for n in code]; assert len(code) <= CODE_SEGMENT_LENGTH; program[:len(code)] = code

computer = IntcodeComputer(None, PrintOutput())
computer.run(program)
