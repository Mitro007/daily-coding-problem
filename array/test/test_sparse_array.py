import random

import pytest

import array.sparse_array as sparse_array
from array.sparse_array import SparseArrayType, SparseArray


class TestSparseArray:
    def test_get_instance(self):
        arr = sparse_array.get_instance(SparseArrayType.DICT_OF_KEYS, [1, 0, 0, 2, 0])
        assert isinstance(arr, SparseArray)

        arr = sparse_array.get_instance(SparseArrayType.LIST_OF_LIST, [1, 0, 0, 2, 0])
        assert isinstance(arr, SparseArray)

    @pytest.mark.parametrize("array_type", [SparseArrayType.DICT_OF_KEYS, SparseArrayType.LIST_OF_LIST])
    def test_sparse_array(self, array_type: SparseArrayType):
        orig_arr = [1, 0, 0, 2, 0]
        arr = sparse_array.get_instance(array_type, orig_arr)

        assert len(arr) == len(orig_arr)
        assert [arr[x] for x in range(len(orig_arr))] == orig_arr

        arr[1] = -1
        assert [arr[x] for x in range(len(orig_arr))] == [1, -1, 0, 2, 0]

        arr[0] = 0
        assert [arr[x] for x in range(len(orig_arr))] == [0, -1, 0, 2, 0]

        arr[3] = 1
        assert [arr[x] for x in range(len(orig_arr))] == [0, -1, 0, 1, 0]

    @pytest.mark.parametrize("array_type", [SparseArrayType.DICT_OF_KEYS, SparseArrayType.LIST_OF_LIST])
    def test_compression_percent(self, array_type: SparseArrayType):
        orig_arr = [0] * 10000
        arr = sparse_array.get_instance(array_type, orig_arr)

        random.seed(1)
        for i in range(10):
            arr[random.randint(0, len(orig_arr) - 1)] = 1

        assert arr.compression_percent() > 90
