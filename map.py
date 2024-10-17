from items import *
from file_manager import *

# location_descriptions.txt FORMAT:
# name // TYPE // exit_1 // leads_to_1 // ... // exit_n // leads_to_n // description

# types of locations
# PUB, COMBAT, JUNCTION, SHOP, STATION

class location: # class for each location on the map
    def __init__(self, n, t, e, d):
        self.name = n
        self.type = t
        self.exits = e
        self.description = d
        self.visited = False # turns True when the user visits this location, so that they don't have to (eg) fight the same wave of enemies twice
        self.items = [] # list of items found at a location
        self.events = [] # list of events which could happen at this location
    
    def is_empty(self): # returns True is all the events for a given location have been completed, else False
        if len(self.events) > 0:
            return False
        return True

class pub(location): 
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)
        data = read_file_where("pubs.txt", n) # FORMAT - name // queue_time (mins) // item_1 // price_1 // ... // item_n // price_n
        self.queue_time = int(data[1])
        menu = {}
        i = 2
        while i < len(data)-1:
            if data[i+2] == "DRINK":
                menu[data[i]] = drink(data[i], float(data[i+1]))
            elif data[i+2] == "FOOD":
                menu[data[i]] = food(data[i], float(data[i+1]))
            i += 3
        self.menu = menu
    
    def print_menu(self):
        for item in self.menu.values():
            if item.type == "FOOD":
                print("£" + str(item.price), "|", item.name)
            elif item.type == "DRINK":
                print("£" + str(item.price), "|", item.name, "(" + str(item.alcohol_units), "units)")
                
class shop(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)
        data = read_file_where("shops.txt", n)
        menu = {}
        i = 1
        while i < len(data):
            menu[data[i]] = shop_item(data[i])
            i += 1
        self.menu = menu
    
    def print_menu(self):
        for item in self.menu.values():
            print("£" + str(item.price), "|", item.name.upper(), "-", item.description)

class combat(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)

class junction(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)

class station(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)

class drink:
    def __init__(self, n, p):
        self.name = n
        self.price = p
        self.type = "DRINK"
        self.alcohol_units = read_file_where("drinks.txt", n)[1] # dictates how drunk the player will get after consumption

class food:
    def __init__(self, n, p):
        self.name = n
        self.price = p
        self.type = "FOOD"
        self.sustinance = read_file_where("foods.txt", n)[1] # dictates how much health a player will gain / how much drunkenness the player will lose

class shop_item:
    def __init__(self, n):
        self.name = n
        data = read_file_where("shop_items.txt", n)
        self.price = data[1]
        self.use = data[2]
        self.amount = data[3]
        self.description = data[4]
        self.num_uses = data[5]
    
    # potential uses of items
    # REDUCE DRUNKENNES, INCREASE HEALTH, INCREASE LUCK, ...

def initialise_locations():
    locations = {}
    data = read_file("location_descriptions.txt")
    for line in data:
        exits = {} # moved exits here
        if len(line) > 3: # meaning some exits exist
            i = 2 # the first exit will be at index 2
            while i < len(line)-1:
                exits[line[i]] = line[i+1]
                i += 2
        if line[1] == "PUB":
            new_loc = pub(line[0], line[1], exits, line[len(line)-1])
        elif line[1] == "SHOP":
            new_loc = shop(line[0], line[1], exits, line[len(line)-1])
        elif line[1] == "COMBAT":
            new_loc = combat(line[0], line[1], exits, line[len(line)-1])
        elif line[1] == "JUNCTION":
            new_loc = junction(line[0], line[1], exits, line[len(line)-1])
        elif line[1] == "STATION":
            new_loc = station(line[0], line[1], exits, line[len(line)-1])
        locations[line[0]] = new_loc
    return locations

def is_valid_exit(l, e): # given the name of the current location, is the chosen exit valid?
    if l in locations and e in locations[l].exits.keys():
        return True
    return False

locations = initialise_locations() # dict of all location objects, indexed by name