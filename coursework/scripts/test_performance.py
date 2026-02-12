"""
Performance test for binary search algorithm.

This test measures:
- Time taken to search for an element
- Size of the array searched
- Results are logged to test_results.txt
"""

import time
import sys
import csv
from datetime import datetime
import importlib.util
import pathlib

# Import the iterative binary search implementation with clear name
module_path = pathlib.Path(__file__).parent / "binary_search_iterative.py"
spec = importlib.util.spec_from_file_location("binary_search_iterative", str(module_path))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
binary_search_iterative = mod.binary_search_iterative


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
    
    print("Running Iterative Binary Search Performance Tests...")
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
        result = binary_search_iterative(arr, target_value)
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
    
    # Append results to the CSV summary only
    with summary.open("a", newline="", encoding="utf-8") as csvf:
        writer = csv.writer(csvf)
        for array_size, target_value in test_cases:
            # find corresponding result in results list by index
            # results are in same order as test_cases
            idx = test_cases.index((array_size, target_value))
            line = results[idx]
            # extract number fields from line
            parts = line.split("|")
            array_size_str = parts[0].split(":")[1].strip()
            target_str = parts[1].split(":")[1].strip()
            index_str = parts[2].split(":")[1].strip()
            time_str = parts[3].split(":")[1].strip().split()[0]
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), module_path.name, "binary_search_iterative", array_size_str, target_str, index_str, time_str])

    print(f"\nResults appended to performance_summary.csv")


if __name__ == "__main__":
    run_performance_tests()
