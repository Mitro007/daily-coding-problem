import pytest

from stack.three_stacks import ThreeStacks


class TestThreeStacks:
    def test_push_and_pop(self):
        stack = ThreeStacks(10)

        for i in range(3):
            assert stack.is_empty(i)

        for i in range(1, 4):
            stack.push(i, 0)

        for i in range(4, 7):
            stack.push(i, 1)

        for i in range(7, 11):
            stack.push(i, 2)

        for i in range(3):
            assert stack.is_full(i)

        assert [stack.pop(i) for i in range(3)] == [3, 6, 10]
        assert [stack.pop(i) for i in range(3)] == [2, 5, 9]
        assert [stack.pop(i) for i in range(3)] == [1, 4, 8]

        for i in range(2):
            assert stack.is_empty(i)

        assert not stack.is_empty(2)
        assert stack.pop(2) == 7
        assert stack.is_empty(2)

    def test_pop_when_empty(self):
        stack = ThreeStacks(10)

        for i in range(3):
            with pytest.raises(RuntimeError):
                stack.pop(i)

    def test_push_when_full(self):
        stack = ThreeStacks(3)
        for i in range(3):
            stack.push(i, i)

        for i in range(3):
            with pytest.raises(RuntimeError):
                stack.push(i, i)
