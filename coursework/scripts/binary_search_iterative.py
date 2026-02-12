"""
Iterative binary search implementation with clear naming.
"""

def binary_search_iterative(arr, target):
    """Iterative binary search returning index or -1."""
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


if __name__ == "__main__":
    arr = [2, 3, 4, 10, 40, 47, 99, 104, 122]
    x = 104
    result = binary_search_iterative(arr, x)
    if result != -1:
        print("Element is present at index", result)
    else:
        print("Element is not present in array")
