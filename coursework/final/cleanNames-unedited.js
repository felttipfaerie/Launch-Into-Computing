// cleanNames.js

function processNames(names) {
    let uniqueNames = [...new Set(names)]; // removes duplicates
    uniqueNames.sort(); // sorts alphabetically
    return uniqueNames;
}

// Test list with duplicates and inconsistent capitalisation
const testNames = ["Alice", "bob", "alice", "Charlie", "BOB", "dave", "Eve", "charlie"];

console.log("Original list:", testNames);
console.log("Processed list:", processNames(testNames));
