from intcode import IntcodeComputer
from io_devices import PrintOutput

def hello_world():
    """
    >>> hello_world()
    123
    """
    computer = IntcodeComputer(None, PrintOutput())
    computer.run([
        # output immediate
        104,
        123,

        # stop
        99,
    ])
