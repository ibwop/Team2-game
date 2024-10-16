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

def initialise_locations():
    locations = {}
    file_data = read_file("location_descriptions.txt")
    exits = {}
    for data in file_data:
        if len(data) > 3: # meaning some exits exist
            i = 2 # the first exit will be at index 2
            while i < len(data)-1:
                exits[data[i]] = data[i+1]
                i += 2
        locations[data[0]] = location(data[0], data[1], exits, data[len(data)-1])
    return locations

def is_valid_exit(l, e): # given the name of the current location, is the chosen exit valid?
    if e in locations[l].exits.keys():
        return True
    return False

locations = initialise_locations() # dict of all location objects, indexed by name