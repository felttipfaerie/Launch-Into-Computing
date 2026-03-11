"""
Performance test for linear search algorithm.

This test measures:
- Time taken to search for an element
- Size of the array searched
- Results are logged to linear_test_results.txt
"""

import time
import sys
import csv
from datetime import datetime
import pathlib
import importlib.util

# Load the linear-search.py module (robust import for hyphenated filename)
module_path = pathlib.Path(__file__).parent / "linear-search.py"
spec = importlib.util.spec_from_file_location("linear_search", str(module_path))
linear_search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linear_search)
linearSearch = linear_search.linearSearch


def run_performance_tests():
    """Run performance tests and log results."""

    results = []

    # Test with arrays of different sizes
    test_cases = [
        (100, 50),
        (1000, 500),
        (10000, 5000),
        (100000, 50000),
        (1000000, 500000),
    ]

    print("Running Linear Search Performance Tests...")
    print("-" * 60)

    # Prepare CSV summary file
    summary = pathlib.Path(__file__).parent / "performance_summary.csv"
    if not summary.exists():
        with summary.open("w", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)
            writer.writerow(["timestamp","module","function","array_size","target","index","time_us"]) 

    for array_size, target_value in test_cases:
        # Create a sorted array
        arr = list(range(1, array_size + 1))

        # Measure search time
        start_time = time.time()
        result = linearSearch(arr, target_value)
        end_time = time.time()

        elapsed_time = (end_time - start_time) * 1000000  # Convert to microseconds

        # Print results
        output_line = (
            f"Array Size: {array_size:>10} | "
            f"Target: {target_value:>10} | "
            f"Found at Index: {result:>10} | "
            f"Time: {elapsed_time:>10.4f} µs"
        )
        print(output_line)
        results.append(output_line)

    print("-" * 60)

    # Write results to file (append mode)
    # Append results to CSV summary only
    with summary.open("a", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        for i, (array_size, target_value) in enumerate(test_cases):
            line = results[i]
            parts = line.split("|")
            array_size_str = parts[0].split(":")[1].strip()
            target_str = parts[1].split(":")[1].strip()
            index_str = parts[2].split(":")[1].strip()
            time_str = parts[3].split(":")[1].strip().split()[0]
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), module_path.name, "linearSearch", array_size_str, target_str, index_str, time_str])

    print(f"\nResults appended to performance_summary.csv")


if __name__ == "__main__":
    run_performance_tests()
