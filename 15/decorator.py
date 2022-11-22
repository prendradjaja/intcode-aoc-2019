def trace(label):
    def decorator(f):
        f.name = label
        return f
    return decorator

class Adder:
    @trace('yo')
    def add(self, x, y):
        return x + y

adder = Adder()
print(adder.add(3, 4))
print(adder.add.name)
