# Import the bisect module
import bisect 

def bisect_search(arr, target):
    index = bisect.bisect_left(arr, target) 
    if index < len(arr) and arr[index] == target:
        return index
    return -1

# Call the module and provide the array and the target value
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = int(input("Enter a number: "))
index = bisect_search(arr, target)

#Print results
if index < len(arr) and arr[index] == target:
    print("found at location ", index + 1)
else:
    print("Bisect: Target not found")




def search(list, n):
    for i in range(len(list)):
        if list[i] == n:
            return i
    return -1


list = ["a", "b", "c", "d", "e"]
n = input("Enter a letter: ")

i = search(list, n)
print("found at location ", i + 1)

