from map import functions as func


class TestMap:
    def test_flatten_dict(self):
        flattened = func.flatten_dict({
            "key": 3,
            "foo": {
                "a": 5,
                "bar": {
                    "baz": 8
                }
            }
        })

        assert flattened == {
            "key": 3,
            "foo.a": 5,
            "foo.bar.baz": 8
        }
