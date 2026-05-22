import pytest
from algorithms import bubble_sort


@pytest.mark.parametrize("input_arr, expected", [
    ([22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31], [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]),
    ([100_000, 123, 129_450, -193, 972, -59, 3], [-193, -59, 3, 123, 972, 100_000, 129_450]),
    ([-23, 98, 0, -3, -5, 145, 2.5], [-23, -5, -3, 0, 2.5, 98, 145]),
])
def test_bubble_sort(input_arr, expected):
    assert bubble_sort(input_arr) == expected