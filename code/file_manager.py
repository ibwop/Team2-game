def read_file(f): # reads the description files, which are lists separated by ' // '
    data = []
    with open(f, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            if len(line) > 0:
                if line[0] != "#":
                    data.append(line.split(" // "))
    return data # data is returned as a list of lines, where each line is a list of strings

def read_file_where(f, name): # reads a file and only returns data for the line where the first item (typically the name) matches the given name
    data = read_file(f)
    for line in data:
        if line[0] == name:
            return line
    print(name)
    return