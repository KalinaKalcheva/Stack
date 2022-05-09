from core.stack_singleton import StackSingleton

stack = StackSingleton()


def is_input_valid(data) -> bool:
    return isinstance(data, int)


def push(data) -> None:
    stack.push(data)


def pop() -> int:
    return stack.pop()


def max() -> int:
    return stack.get_max()


def get_stack() -> list:
    return stack.get_stack()


def is_empty() -> bool:
    return stack.is_empty()
