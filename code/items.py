from file_manager import *

# items_descriptions.txt FORMAT:
# name // description

class item:
    def __init__(self, n, d, l, x):
        self.name = n
        self.description = d
        self.location = l
        self.damage = x

def initialise_items():
    data = read_file("text/items_descriptions.txt")
    items = {}
    for i in data:
        try:
            name, description, location, damage = i
            items[name] = item(name, description, location, damage)
        except ValueError:
            print(f"Skipping line due to unpacking error: {i}")
    return items

items_list = initialise_items() # dict of all item objects, indexed by name