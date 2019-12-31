from typing import List


# 141. Implement 3 stacks using a single list:
# class Stack:
#     def __init__(self):
#         self.list = []
#
#     def pop(self, stack_number):
#         pass
#
#     def push(self, item, stack_number):
#         pass
#
# ANSWER: One obvious solution is given array size n, divide up n into 3 parts, and allocate floor(n / 3) cells
# to two stacks at either end of the array, and remaining cells to the one in the middle. This strategy is not
# space efficient because even though there may be space in the array, one of the stack may overflow.
#
# A better approach is to have two stacks at either end of the array, the left one growing on the right, and the
# right one growing on the left. The middle one starts at index floor(n / 2), and grows at both ends. When the
# middle stack size is even, it grows on the right, and when it's odd, it grows on the left. This way, the middle
# stack grows evenly and minimizes the changes of overflowing one of the stack at either end.
#
# The rest is pointer arithmetic, adjusting tops of the stacks on push and pop operations.
class ThreeStacks:
    def __init__(self, n: int):
        self._arr: List[int] = [0] * n
        self._tops: List[int] = [-1, n, n // 2]
        self._sizes: List[int] = [0] * 3
        self._n = n

    def _is_stack_3_even_size(self):
        return self._sizes[2] % 2 == 0

    def _is_stack_3_odd_size(self):
        return not self._is_stack_3_even_size()

    def is_empty(self, stack_number: int) -> bool:
        return self._sizes[stack_number] == 0

    def is_full(self, stack_number: int) -> bool:
        if stack_number == 0 and self._is_stack_3_odd_size():
            return self._tops[stack_number] == self._tops[2] - self._sizes[2]
        elif stack_number == 1 and self._is_stack_3_even_size():
            return self._tops[stack_number] == self._tops[2] + self._sizes[2]

        return (self._is_stack_3_odd_size() and self._tops[0] == self._tops[2] - self._sizes[2]) or \
               (self._is_stack_3_even_size() and self._tops[1] == self._tops[2] + self._sizes[2])

    def pop(self, stack_number: int) -> int:
        if self.is_empty(stack_number):
            raise RuntimeError(f"Stack : {stack_number} is empty")

        x: int = self._arr[self._tops[stack_number]]
        if stack_number == 0:
            self._tops[stack_number] -= 1
        elif stack_number == 1:
            self._tops[stack_number] += 1
        else:
            if self._is_stack_3_even_size():
                self._tops[stack_number] += (self._sizes[stack_number] - 1)
            else:
                self._tops[stack_number] -= (self._sizes[stack_number] - 1)

        self._sizes[stack_number] -= 1
        return x

    def push(self, item: int, stack_number: int) -> None:
        if self.is_full(stack_number):
            raise RuntimeError(f"Stack: {stack_number} is full")

        if stack_number == 0:
            self._tops[stack_number] += 1
        elif stack_number == 1:
            self._tops[stack_number] -= 1
        else:
            if self._is_stack_3_even_size():
                self._tops[stack_number] += self._sizes[stack_number]
            else:
                self._tops[stack_number] -= self._sizes[stack_number]
        self._arr[self._tops[stack_number]] = item
        self._sizes[stack_number] += 1

    def __repr__(self):
        return str(self._arr)
