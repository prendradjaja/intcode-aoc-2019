from abc import ABC, abstractmethod

# Abstract base classes

class Input(ABC):
    @abstractmethod
    def get_value(self):
        pass


class Output(ABC):
    @abstractmethod
    def put_value(self, value):
        pass


# Input devices


OneValueInput = lambda value: FixedValuesInput([value])


class FixedValuesInput(Input):
    def __init__(self, values):
        self.iterator = iter(values)

    def get_value(self):
        return next(self.iterator)


class CallbackInput(Input):
    def __init__(self, cb):
        self.cb = cb

    def get_value(self):
        return self.cb()


# Output devices

class PrintOutput(Output):
    def put_value(self, value):
        print(value)


# TODO name
class OneValueStore(Output):
    def put_value(self, value):
        self.value = value


class QueueStore(Input, Output):
    def __init__(self):
        self.values = []

    def get_value(self):
        return self.values.pop(0)

    def put_value(self, value):
        self.values.append(value)


class CallbackOutput(Output):
    def __init__(self, cb):
        self.cb = cb

    def put_value(self, value):
        self.cb(value)
