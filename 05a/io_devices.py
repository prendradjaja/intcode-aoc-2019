from abc import ABC, abstractmethod

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
