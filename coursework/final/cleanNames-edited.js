// cleanNames.js

function processNames(names) {
    names = names.map(name => name.toLowerCase()); // Normalize names to lowercase
    let uniqueNames = [...new Set(names)]; // removes duplicates
    uniqueNames.sort(); // sorts alphabetically
    return uniqueNames;
}

// Test list with duplicates and inconsistent capitalisation
const testNames = ["Alice", "1234", "bob", "alice", "Charlie", "BOB", "dave", "Eve", "charlie"];

console.log("Original list:", testNames);
console.log("Processed list:", processNames(testNames));
