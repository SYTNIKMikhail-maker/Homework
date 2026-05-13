from algorithms import binary_search

# Test datasets (pre-sorted)
expected1 = [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]
expected2 = [-193, -59, 3, 123, 972, 100_000, 129_450]


def test_binary_search():
    # Test binary search on sorted arrays.
    assert binary_search(expected1, 22) == 5
    assert binary_search(expected1, 1) == 0
    assert binary_search(expected1, 99) == -1
    assert binary_search(expected2, -193) == 0
    assert binary_search(expected2, 999) == -1
    print("Binary search is normal")


test_binary_search()