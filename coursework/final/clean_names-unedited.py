# clean_names.py
# all code can be found at: https://github.com/felttipfaerie/Launch-Into-Computing/tree/master/coursework/final

def process_names(names):
    unique_names = list(set(names))  # removes duplicates but doesn't preserve order
    unique_names.sort()  # sorts alphabetically
    return unique_names

# Test list with duplicates and inconsistent capitalisation
test_names = ["Alice", "bob", "alice", "Charlie", "BOB", "dave", "Eve", "charlie"]

print("Original list:", test_names)
print("Processed list:", process_names(test_names))
