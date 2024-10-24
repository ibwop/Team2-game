from file_manager import *

# items_descriptions.txt FORMAT:
# name // description

class item:
    def __init__(self, data):
        self.name = data[0]
        self.description = data[1]
        self.location_found = data[2]
        self.is_weapon = bool(int(data[3]))
        if self.is_weapon:
            self.range = bool(int(data[4]))
            self.group = bool(int(data[5]))
            self.damage = float(data[6])

def initialise_items():
    data = read_file(r"..\text\items_descriptions.txt")
    items = {}
    for i in data:
        items[i[0]] = item(i) # i[2], i[3])
    return items

items_list = initialise_items() # dict of all item objects, indexed by name