from design.peekable_iterator import PeekableIterator


class TestPeekableIterator:
    def test_peekable_iterator(self):
        it = iter(range(5))
        pit = PeekableIterator(it)

        elements = []
        while True:
            x = pit.peek()
            if x is not None:
                elements.append(x)
            else:
                break

        assert elements == list(pit)
