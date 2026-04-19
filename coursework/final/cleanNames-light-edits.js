// cleanNames-light-edits.js
// all code can be found at: https://github.com/felttipfaerie/Launch-Into-Computing/tree/master/coursework/final
function isValidName(name) {
    return /^(?=.*\p{L})[\p{L}\p{M}\s'-]+$/u.test(name);
} //handels names with letters, spaces, hyphens, and apostrophes, and ensures that there is at least one letter in the name. It also supports names from various languages by using Unicode property escapes.

function printInvalidNames(names) {
    const invalidNames = names.filter(name => !isValidName(name));
    return invalidNames.join(", ");
} // This function filters out invalid names from the original list and returns them as a comma-separated string, allowing us to see which entries were considered invalid and why they were filtered out.

function processNames(names) {
    const lowercasedNames = names.map(name => name.toLowerCase()); // added lowercase to ensure consistent capitalisation and prevent duplicates
    // const added to prevent overwriting
    const validNames = lowercasedNames.filter(isValidName); // filters out invalid names
    const uniqueNames = [...new Set(validNames)]; // const added to prevent overwriting
    uniqueNames.sort();
    return uniqueNames;
}

// Test list with duplicates and inconsistent capitalisation
const testNames = ["Alice", "bob", "Eleanor-Rose", "McDonald", "O'Conner", "François", "Дмитро́", "محمد", "##:)", "Big D", "!@#", "1234", "alice", "Charlie", "BOB", "dave", "Eve", "charlie"];
//additional names added to test the function's ability to handle non-name and non-western alphabet entries and ensure they are processed correctly

console.log("Original list: (" + testNames.length + "):", testNames.join(", "));
console.log("Processed list: (" + processNames(testNames).length + "):", processNames(testNames).join(", "));
console.log("Invalid names: (" + (testNames.length - processNames(testNames).length) + "):", printInvalidNames(testNames)); // view invalid names and their count to understand what was filtered out