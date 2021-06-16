import collections

class Memory:
    """
    A sliceable defaultdict(int)

    >>> m = Memory()
    >>> m[0] += 1
    >>> m[0]
    1
    >>> m.load([3, 4, 5])
    >>> m[:5]
    [3, 4, 5, 0, 0]
    """

    def __init__(self):
        self._memory = collections.defaultdict(int)

    def load(self, values):
        for i, value in enumerate(values):
            self._memory[i] = value

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._memory[key]
        elif isinstance(key, slice):
            indices = range(*key.indices(key.stop))
            return [self._memory[i] for i in indices]
        else:
            1/0

    def __setitem__(self, key, value):
        self._memory[key] = value
