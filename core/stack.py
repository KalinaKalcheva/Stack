class Stack:
    def __init__(self):
        self._data = []
        self._max_stack = []

    def push(self, item) -> None:
        self._data.append(item)
        if self.is_empty() or item >= self.get_max():
            self._max_stack.append(item)

    def pop(self) -> int:
        last = self._data.pop()
        if last == self.get_max():
            self._max_stack.pop()
        return last

    def get_max(self) -> int:
        return self._max_stack[-1]

    def is_empty(self) -> bool:
        return len(self._max_stack) == 0

    def get_stack(self) -> list:
        return self._data


