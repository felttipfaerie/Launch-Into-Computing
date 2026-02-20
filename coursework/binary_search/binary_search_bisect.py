"""
Bisect-based binary search implementation with clear naming.
"""
import bisect


def binary_search_bisect(arr, target):
    """Binary search using bisect.bisect_left."""
    i = bisect.bisect_left(arr, target)
    if i < len(arr) and arr[i] == target:
        return i
    return -1


if __name__ == "__main__":
    arr = [2, 3, 4, 10, 40, 47, 99, 104, 122]
    x = 104
    result = binary_search_bisect(arr, x)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")
