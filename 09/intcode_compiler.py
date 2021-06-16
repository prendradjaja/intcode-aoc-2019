class VariableAllocator:
    def __init__(self, code_segment_length, data_segment_length, program):
        self.code_segment_length = code_segment_length
        self.data_segment_length = data_segment_length
        self.program = program  # This will be mutated

        self.nvars = 0

    def make_var(self, initial_value):
        address = self.nvars + self.code_segment_length
        self.program[address] = initial_value
        self.nvars += 1
        return address
