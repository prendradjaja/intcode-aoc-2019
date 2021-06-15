from abc import ABC, abstractmethod


class Input(ABC):
    @abstractmethod
    def get_value(self):
        pass


class Output(ABC):
    @abstractmethod
    def put_value(self, value):
        pass


class OneValueInput(Input):
    def __init__(self, value):
        self.called = False
        self.value = value

    def get_value(self):
        assert not self.called
        self.called = True
        return self.value


class PrintOutput(Output):
    def put_value(self, value):
        print(value)
