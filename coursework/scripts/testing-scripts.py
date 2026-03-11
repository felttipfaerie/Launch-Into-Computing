n = 0
a = "*"

""""

def triangle():
    global n
    global a
    while n < 9:
        print(a)
        a = a + "*"
        n = n + 1

triangle()

def diamond():
    global n
    global a
    for i in range(0, 5):
        print(a)
        a = a + "*"

    """""

def triangle(n):
    j = 0
    list = []
    for i in range(1, n + 1):
        while j < i:
            list.append("▲")
            delimiter = " " # Define a delimiter to join the elements of the list
            line_string = map(str, list) # Convert each element in the list to a string
            joined_line = delimiter.join(line_string) # Join the elements of the list into a single string with the delimiter
            print(f"{joined_line}")
            j = j + 1
triangle(3)


def diamond(n):
    j = 0
    m = n / 2
    list = []
    for i in range(1, m + 1):
        while j < i:
                list.append("♦")
                j = j + 1
                return list
    print(list)

diamond(5)