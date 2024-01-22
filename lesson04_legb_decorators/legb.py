name = "John"
print(id(name))


def change_john_to_marry(name: str):
    name = "Marry"
    print(id(name))


def parabola(x: int) -> int:
    result = x ** 2
    return result


change_john_to_marry(name)
print(id(name))
