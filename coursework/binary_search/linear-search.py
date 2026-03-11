"""
Linear Search Algorithm Implementation

This module implements the linear search algorithm for finding a target value
in a list.
"""


def linearSearch(arr, target):
    """
    Search for target in an array using linear search.

    Args:
        arr (list): A list of comparable elements
        target: The value to search for

    Returns:
        int: The index of target if found, -1 otherwise
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


if __name__ == "__main__":
    # Example usage
    numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    print("Linear Search Example")
    print(f"Array: {numbers}\n")

    target = 13
    result = linearSearch(numbers, target)
    print(f"Linear Search for {target}: Index {result}")

    target = 20
    result = linearSearch(numbers, target)
    print(f"Linear Search for {target}: Index {result}")
