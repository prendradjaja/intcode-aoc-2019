from abc import ABC, abstractmethod

# TODO Split inputs apart from outputs

class IO(ABC):
    @abstractmethod
    def input(self):
        pass

    @abstractmethod
    def output(self, value):
        pass

# Day 5
class ThermalEnvironmentSupervisionTerminalIO(IO):
    def __init__(self):
        self.input_called = False

    def input(self):
        assert not self.input_called
        self.input_called = True
        return 1

    def output(self, value):
        print(value)

class OneInputAndPrintIO(IO):
    def __init__(self, value):
        self.input_called = False
        self.value = value

    def input(self):
        assert not self.input_called
        self.input_called = True
        return self.value

    def output(self, value):
        print(value)
