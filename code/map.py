from game import *
from file_manager import *
import os

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
    
    def print_exits(self):
        for ex in self.exits.keys():
            if ex == "train":
                print("TAKE TRAIN to", self.exits[ex])
            else:
                print("GO", ex.upper(), "to", self.exits[ex])
    
    def go_inside(self):
        print("You are now inside", self.name)

class Pub(location): 
    def __init__(self, name, loc_type, exits, description):
        # Initialize the location base class
        location.__init__(self, name, loc_type, exits, description)
        
        # Read pub data from file (format: name // queue_time // item_1 // price_1 // ... // item_n // price_n)
        pub_data = read_file_where("text/pubs.txt", name)
        
        # set queue time (in minutes)
        self.queue_time = int(pub_data[1])

        # initialize the pub's menu
        self.menu = self._initialize_menu(pub_data[2:])

    def _initialize_menu(self, data):
        """ Helper function to initialize the pub menu. """
        menu = {}
        index = 0
        
        # Process each item from the data
        while index < len(data) - 2:
            item_name = data[index]
            item_price = float(data[index + 1])
            item_type = data[index + 2]
            
            # Add either a drink or food item to the menu based on type
            if item_type == "DRINK":
                menu[item_name] = drink(item_name, item_price)
            elif item_type == "FOOD":
                menu[item_name] = food(item_name, item_price)

            # Move to the next item (each item block consists of 3 elements: name, price, type)
            index += 3
        
        return menu

    
    def print_menu(self):
        for item in self.menu.values():
            if item.type == "FOOD":
                print("£" + str(item.price), "|", item.name)
            elif item.type == "DRINK":
                print("£" + str(item.price), "|", item.name, "(" + str(item.alcohol_units), "units)")

    
    def go_inside(self):
        self.print_menu()
        print("or LEAVE")
    
    def execute_inside(self, inp, money): # returns price of item bought (or 0 if nothing), whether or not the player chose to leave the building
        inp = " ".join(inp)
        for item in self.menu.values():
            if inp == item.name.lower():
                if money >= item.price:
                    item.consume()
                    # update time based on a wait time and consumption time
                    return -item.price, False
                else:
                    print("You cannot afford this.")
                return 0, False
        if inp == "leave":
            return 0, True
        else:
            print("Item not available.")
            return 0, False
                
class shop(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)
        data = read_file_where("text/shops.txt", n)
        menu = {}
        i = 1
        while i < len(data):
            menu[data[i]] = shop_item(data[i])
            i += 1
        self.menu = menu
    
    def print_menu(self):
        for item in self.menu.values():
            print("£" + str(item.price), "|", item.name.upper(), "-", item.description)
    
    def go_inside(self):
        self.print_menu()
        print("or LEAVE")
    
    def execute_inside(self, inp, money):
        inp = " ".join(inp)
        for item in self.menu.values():
            if inp == item.name.lower():
                if money >= item.price:
                    item.buy()
                    return -item.price, False, item
                else:
                    print("You cannot afford this.")
                return 0, False, None
        if inp == "leave":
            return 0, True, None
        else:
            print("Item not available.")
            return 0, False, None

class combat(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)
    
    def menu(self):
        print()
        print(self.fight_description)
        print()
        fighting = True
        while fighting:
            for item in self.items_inventory:
                pass
    
class enemy:
    def __init__(self, descriptions, weapon):
        self.name = descriptions[0]
        self.description = descriptions[1]
        self.health = descriptions[2]
        self.damage = weapon[0]
        self.range = weapon[1]

class weapon:
    def __init__(self, n, d, r, g):
        self.name = n
        self.damage = d # float containing how much damage is done
        self.range = r # text saying whether it is CLOSE or FAR range
        self.group = g # boolean, True if it can damage multiple enemies at once

class junction(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)

class station(location):
    def __init__(self, n, t, e, d):
        location.__init__(self, n, t, e, d)

class drink:
    def __init__(self, n, p):
        self.name = n
        self.price = float(p)
        self.type = "DRINK"
        self.alcohol_units = float(read_file_where("text/drinks.txt", n)[1]) # dictates how drunk the player will get after consumption
    
    def consume(self):
        print("DRINKING", self.name)

class food:
    def __init__(self, n, p):
        self.name = n
        self.price = float(p)
        self.type = "FOOD"
        self.sustinance = float(read_file_where("text/foods.txt", n)[1]) # dictates how much health a player will gain / how much drunkenness the player will lose
    
    def consume(self):
        print("EATING", self.name)

class shop_item:
    def __init__(self, n):
        self.name = n
        data = read_file_where("text\shop_items.txt", n)
        self.price = float(data[1])
        self.use = data[2]
        self.amount = float(data[3])
        self.description = data[4]
        self.num_uses = int(data[5])
    
    def buy(self):
        print("You have bought", self.name)
    
    # potential uses of items
    # REDUCE DRUNKENNES, INCREASE HEALTH, INCREASE LUCK, ...

def initialise_locations():
    locations = {}  # dictionary to store locations
    data = read_file("text/location_descriptions.txt")

    for line in data:
        exits = {}  # initiase exits for each location

        location_id = line[0] 
        location_type = line[1]  # (e.g. PUB, SHOP)
        description = line[-1] 
        
        # If there are exits 
        if len(line) > 3:
            i = 2  # Exits start at index 2
            while i < len(line) - 1:
                direction = line[i]  # direction of exit
                destination = line[i + 1]  # destination the exit leads to
                exits[direction] = destination  # map direction to destination
                i += 2

        # ceate location type based on the value of location_type
        if location_type == "PUB":
            new_loc = Pub(location_id, location_type, exits, description)
        elif location_type == "SHOP":
            new_loc = shop(location_id, location_type, exits, description)
        elif location_type == "COMBAT":
            new_loc = combat(location_id, location_type, exits, description)
        elif location_type == "JUNCTION":
            new_loc = junction(location_id, location_type, exits, description)
        elif location_type == "STATION":
            new_loc = station(location_id, location_type, exits, description)

        # add new location to the locations dictionary
        locations[location_id] = new_loc

    return locations

def is_valid_exit(l, e): # given the current location, is the chosen exit valid?
    if e in l.exits.keys():
        return True
    return False

locations = initialise_locations()