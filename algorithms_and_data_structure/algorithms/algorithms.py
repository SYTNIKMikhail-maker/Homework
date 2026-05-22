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