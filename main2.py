array = []
with open(".adatok", "r") as file:
    for line in file:
        line = line.strip("\n")
        if len(line) == 1:
            array.append(line)
        if "waiting list " in line:
            array.append(line)
    for item in array:
        print(item)