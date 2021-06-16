from abc import ABC, abstractmethod


class Input(ABC):
    @abstractmethod
    def get_value(self):
        pass


class Output(ABC):
    @abstractmethod
    def put_value(self, value):
        pass


OneValueInput = lambda value: FixedValuesInput([value])


class FixedValuesInput(Input):
    def __init__(self, values):
        self.iterator = iter(values)

    def get_value(self):
        return next(self.iterator)


class PrintOutput(Output):
    def put_value(self, value):
        print(value)
