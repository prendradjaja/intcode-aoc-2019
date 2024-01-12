from puzzle_inputs import day_17_program as program
from intcode import IntcodeComputer
from io_devices import Input, Output, QueueStore, FixedValuesInput


def main():
    # Solved by hand with a visual aid (spreadsheet)
    # https://docs.google.com/spreadsheets/d/1-TC2uErhxfL_2ezge3BYiwD1g5lti3QJE5qkjLSE3DQ/edit?usp=sharing

    twenty_chars = '....................'
    main_routine = 'A,B,A,C,C,A,B,C,B,B'
    routine_a    = 'L,8,R,10,L,8,R,8'
    routine_b    = 'L,12,R,8,R,8'
    routine_c    = 'L,8,R,6,R,6,R,10,L,8'
    video = 'n'

    assert len(main_routine) <= 20
    assert len(routine_a) <= 20
    assert len(routine_b) <= 20
    assert len(routine_c) <= 20

    text_input = '\n'.join([main_routine, routine_a, routine_b, routine_c, video, ''])
    ascii_input = [ord(ch) for ch in text_input]
    program[0] = 2

    computer = IntcodeComputer(
        input_ = FixedValuesInput(ascii_input),
        output = QueueStore()
    )
    computer.run(program)

    dust = computer.output.values.pop()
    text = ''
    for each in computer.output.values:
        text += chr(each)

    for line in text.splitlines():
        for ch in line:
            print(ch, end=' ')
        print()

    print('Dust:', dust)


if __name__ == '__main__':
    main()
