from file_manager import *

# items_descriptions.txt FORMAT:
# name // description

class item:
    def __init__(self, n, d):
        self.name = n
        self.description = d

def initialise_items():
    data = read_file("items_descriptions.txt")
    items = {}
    for i in data:
        items[i[0]] = item(i[0], i[1])
    return items

items_list = initialise_items() # dict of all item objects, indexed by name