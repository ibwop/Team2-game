class location:
    def __init__(self, n, t, e, d):
        self.name = n
        self.type = t
        self.exits = e
        self.description = d
        self.visited = False

def initialise_locations():
    locations = {}
    with open("location_descriptions.txt", "r") as file:
        for line in file:
            line = line.replace("\n", "")
            data = line.split(" // ")
            exits = {}
            if len(data) > 3:
                i = 2
                while i < len(data)-1:
                    exits[data[i]] = data[i+1]
                    i += 2
            locations[data[0]] = location(data[0], data[1], exits, data[len(data)-1])
    return locations

def is_valid_exit(l, e):
    if e in locations[l].exits.keys():
        return True
    return False

locations = initialise_locations()