from algorithms import quicksort

# Test datasets
dataset1 = [22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31]
expected1 = [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]

dataset2 = [100_000, 123, 129_450, -193, 972, -59, 3]
expected2 = [-193, -59, 3, 123, 972, 100_000, 129_450]

dataset3 = [-23, 98, 0, -3, -5, 145, 2.5]
expected3 = [-23, -5, -3, 0, 2.5, 98, 145]


def test_quicksort():
    # Test quicksort with three datasets.
    assert quicksort(dataset1) == expected1
    assert quicksort(dataset2) == expected2
    assert quicksort(dataset3) == expected3
    print("Quicksort is normal")


test_quicksort()