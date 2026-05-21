import pytest
from algorithms import binary_search

sorted1 = [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]
sorted2 = [-193, -59, 3, 123, 972, 100_000, 129_450]


@pytest.mark.parametrize("arr, target, expected", [
    (sorted1, 22, 5),
    (sorted1, 1, 0),
    (sorted1, 99, -1),
    (sorted2, -193, 0),
    (sorted2, 999, -1),
])
def test_binary_search(arr, target, expected):
    assert binary_search(arr, target) == expected