from file_manager import *
import os

# items_descriptions.txt FORMAT:
# name // description

class item:
    def __init__(self, n, d): # l, dam):
        self.name = n
        self.description = d
        #self.location_found = l
        #self.damage = dam

def initialise_items():
    data = read_file(r"..\text\items_descriptions.txt")
    items = {}
    for i in data:
        items[i[0]] = item(i[0], i[1]) # i[2], i[3])
    return items

items_list = initialise_items() # dict of all item objects, indexed by name