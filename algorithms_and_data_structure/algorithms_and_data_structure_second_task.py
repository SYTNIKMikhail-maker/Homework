# Searching and sorting algorithms. Includes: binary_search, bubble_sort, factorial, quicksort.

def binary_search(arr, target):
    # Binary search in sorted array. O(log n). Returns index or -1.
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def bubble_sort(arr):
    # Bubble sort. O(n^2). Returns new sorted list.
    arr = arr[:]
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def factorial(n):
    # Recursive factorial. O(n). Returns n!
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def quicksort(arr):
    # Iterative quicksort using stack. O(n log n) average.
    arr = arr[:]
    if len(arr) <= 1:
        return arr
    stack = [(0, len(arr) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        mid = i + 1
        stack.append((low, mid - 1))
        stack.append((mid + 1, high))
    return arr

# Test datasets
dataset1 = [22, 96, 2, 1, 2, 67, 68, 25, 17, 5, 31]
expected1 = [1, 2, 2, 5, 17, 22, 25, 31, 67, 68, 96]

dataset2 = [100_000, 123, 129_450, -193, 972, -59, 3]
expected2 = [-193, -59, 3, 123, 972, 100_000, 129_450]

dataset3 = [-23, 98, 0, -3, -5, 145, 2.5]
expected3 = [-23, -5, -3, 0, 2.5, 98, 145]

def test_bubble_sort():
    # Test bubble sort with three datasets.
    assert bubble_sort(dataset1) == expected1
    assert bubble_sort(dataset2) == expected2
    assert bubble_sort(dataset3) == expected3
    print("Bubble sort is normal")

def test_binary_search():
    # Test binary search on sorted arrays.
    assert binary_search(expected1, 22) == 5
    assert binary_search(expected1, 1) == 0
    assert binary_search(expected1, 99) == -1
    assert binary_search(expected2, -193) == 0
    assert binary_search(expected2, 999) == -1
    print("Binary search is normal")

def test_factorial():
    # Test factorial with various inputs.
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(10) == 3628800
    print("Factorial is normal")

def test_quicksort():
    # Test quicksort with three datasets.
    assert quicksort(dataset1) == expected1
    assert quicksort(dataset2) == expected2
    assert quicksort(dataset3) == expected3
    print("Quicksort is normal")

# Run all tests
test_bubble_sort()
test_binary_search()
test_factorial()
test_quicksort()
print("All tests were passed")