def read_file(f): # reads the description files, which are lists separated by ' // '
    data = []
    with open(f, "r") as file:
        for line in file:
            line = line.replace("\n", "")
            data.append(line.split(" // "))
    return data # data is returned as a list of lines, where each line is a list of strings