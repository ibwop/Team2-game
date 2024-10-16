from map import *
from items import *
from file_manager import *

class stat:
    def __init__(self, n, d):
        self.name = n
        self.description = d
        self.points = 1 # initial value for each stat (users will allocate an amount of points to some stats)
    
    def inc_points(amount): # used if the user chooses to favour this stat
        self.points += amount

def allocate_points(): # the user can choose which stats to favour
    pass

def initialise_stats():
    data = read_file("stats_descriptions.txt")
    stats = {}
    for line in data:
        stats[line[0]] = stat(line[0], line[1])
    return stats

current_location = locations["Central Bar"] # stores player's current location, starting with Central Bar

inventory = [items_list["Rubber Chicken"]] # stores the items a player currently holds
                 
stats = initialise_stats()