from intcode import IntcodeComputer
from io_devices import FixedValuesInput, QueueStore
from intcode_compiler import *

CODE_SEGMENT_LENGTH = 100
DATA_SEGMENT_LENGTH = 100
'';                                                                                                 program = [0] * (CODE_SEGMENT_LENGTH + DATA_SEGMENT_LENGTH); va = VariableAllocator(CODE_SEGMENT_LENGTH, DATA_SEGMENT_LENGTH, program)

item                = va.make_var(0)
state               = va.make_var(0)
itemstate           = va.make_var(0)
length              = va.make_var(0)
jumpcond            = va.make_var(0)

# LOOP:
#     inp item
#     if item is -1 goto AFTER_LOOP
#     itemstate = item*2 + state
#     if item == 0 and state == 1 i.e. itemstate == 1 goto END_OF_ONES
#     if item == 1 and state == 1 i.e. itemstate == 2 goto ADD_ONE
#     if item == 1 and state == 0 i.e. itemstate == 3 goto START_OF_ONES
# LOOP_END:
#     state = item
#     goto LOOP
#
# AFTER_LOOP:
#     if state == 0 goto PROGRAM_END
#     out length
# PROGRAM_END:
#     halt
#
# END_OF_ONES:
#     out length
#     goto LOOP_END
# ADD_ONE:
#     add 1 to length
#     goto LOOP_END
# START_OF_ONES:
#     set length to 1
#     goto LOOP_END


code = [
];LOOP                                                                                              = len(code); code += [
    *inp(pos(item)),

    *eq(imm(-1), pos(item), pos(jumpcond)),
    *jnz(pos(jumpcond), imm(lambda: AFTER_LOOP)),

    # itemstate = item*2 + state
    *mul(imm(2), pos(item), pos(itemstate)),
    *add(pos(state), pos(itemstate), pos(itemstate)),    
    # if item == 0 and state == 1 goto END_OF_ONES
    *eq(imm(1), pos(itemstate), pos(jumpcond)),
    *jnz(pos(jumpcond), imm(lambda: END_OF_ONES)),
    # if item == 1 and state == 0 goto START_OF_ONES
    *eq(imm(2), pos(itemstate), pos(jumpcond)),
    *jnz(pos(jumpcond), imm(lambda: START_OF_ONES)),
    # if item == 1 and state == 1 goto ADD_ONE
    *eq(imm(3), pos(itemstate), pos(jumpcond)),
    *jnz(pos(jumpcond), imm(lambda: ADD_ONE)),
];LOOP_END                                                                                       = len(code); code += [
    *add(imm(0), pos(item), pos(state)),
    *jnz(imm(1), imm(lambda: LOOP)),

];AFTER_LOOP                                                                                       = len(code); code += [
    # if state == 0 goto PROGRAM_END
    *eq(imm(0), pos(state), pos(jumpcond)),
    *jnz(pos(jumpcond), imm(lambda: PROGRAM_END)),

    *out(pos(length)),
];PROGRAM_END                                                                                       = len(code); code += [
    *halt(),

];END_OF_ONES                                                                                       = len(code); code += [
    *out(pos(length)),
    *jnz(imm(1), imm(lambda: LOOP_END)),
];ADD_ONE                                                                                       = len(code); code += [
    *add(imm(1), pos(length), pos(length)),
    *jnz(imm(1), imm(lambda: LOOP_END)),
];START_OF_ONES                                                                                       = len(code); code += [
    *add(imm(1), imm(0), pos(length)),
    *jnz(imm(1), imm(lambda: LOOP_END)),
];                                                                                                  code = [n if isinstance(n, int) else n() for n in code]; assert len(code) <= CODE_SEGMENT_LENGTH; program[:len(code)] = code

# print(LOOP_END, 'loop-end')
# print(AFTER_LOOP, 'after-loop')
# print(ONE_TO_ZERO, 'one-tozero')
# print(ADD_ONE, 'addone')
# print(START_OF_ONES, 'setone')

def nonogramrow(items):
    items = items[:] + [-1]
    output = QueueStore()
    computer = IntcodeComputer(FixedValuesInput(items), output)
    computer.run(program)
    return output.values

if __name__ == '__main__':
    print(nonogramrow([1,1,1,1,1]))
