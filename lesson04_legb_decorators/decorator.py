# DRY


def error_handler(func):
    some_values = "inside error handler"

    def inner(value: str):
        nonlocal some_values
        some_values += " some words"
        print(some_values)
        try:
            result = func(value=value)
        except ValueError:
            print("Something went wrong")
        else:
            return result

    return inner


# @error_handler
# def greeting(name: str):
#    print(f'Hola, {name}')

# error_handler(greeting)(name= 'Dima')


@error_handler
def make_integer(value: str) -> int:
    return int(value)


@error_handler
def make_float(value: str) -> float:
    return float(value)


value_a = "12.s"
value_b = "12"

print(make_integer(value_b))
print(make_float(value_a))
