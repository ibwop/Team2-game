import game
from file_manager import *
import os
import string
import random

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
        pub_data = read_file_where(r"..\text\pubs.txt", name)
        
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
        data = read_file_where(r"..\text\shops.txt", n)
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
        data = read_file(os.path.join(r"..\combat_descriptions", self.name + ".txt"))
        self.fight_description = data[0][0]
        self.max_distance = int(data[1][1])
        self.distance_to_enemies = int(data[1][1])
        self.enemy_data = {"name": data[2][0],
                           "description": data[2][1],
                           "health": int(data[2][2]),
                           "range_damage": int(data[3][0]),
                           "close_damage": int(data[3][1])}
        self.items_inventory = []
        self.close_range = 30
        self.player_move_distance = 20
        self.enemy_move_distance = 10
        i = 0
        while i < len(data[4]):
            self.items_inventory.append(weapon(data[4][i], data[4][i+1], data[4][i+2], data[4][i+3]))
            i += 4
        self.enemies = self.initialise_enemies(int(data[1][0])) # number of starting enemies
    
    def go_inside(self):
        print()
        print(self.fight_description)
        print()
        self.execute_inside()
    
    def initialise_enemies(self, num):
        enemies = []
        for i in range(num):
            enemies.append(enemy(self.enemy_data))
        return enemies
    
    def take_input(self):
        print("\nThe", len(self.enemies), self.enemy_data["name"] + "(s) are", self.distance_to_enemies, "metres away.\n")
        options = []
        if self.distance_to_enemies > 0:
            options.append("move closer")
        if self.distance_to_enemies < self.max_distance:
            options.append("move away")
        for item in self.items_inventory:
            options.append("pick up " + item.name.lower())
        for item in game.player.inventory:
            options.append("use " + item.name.lower())
            options.append("drop " + item.name.lower())
        for o in options:
            print(o.upper())
        user_input = self.normalise_input(input("What would you like to do?\n"))
        return user_input, options
    
    def execute_inside(self):
        move_count = 0
        fighting = True
        while fighting:
            inp, options = self.take_input()
            if inp in options:
                move_count += 1
                self.execute_inp(inp)
                if self.distance_to_enemies > self.close_range:
                    self.deal_to_player(self.enemy_data["range_damage"])
                else:
                    self.deal_to_player(self.enemy_data["close_damage"])
            else:
                print("Not a valid command.")
            if len(self.enemies) == 0:
                fighting = False
                self.win()
            elif game.player.health.health <= 0:
                fighting = False
                self.lose()
        print(move_count, "minutes")
    
    def win(self):
        print("YOU WON THE FIGHT.")
        self.visited = True
        
    def lose(self):
        print("YOU LOST THE FIGHT.")
        self.visited = True
    
    def execute_inp(self, inp):
        words = inp.split()
        if words[0] == "move":
            if words[1] == "closer":
                self.update_distance_to_enemies(-self.player_move_distance)
                return
            else:
                self.update_distance_to_enemies(self.player_move_distance)
                return
        elif words[0] == "pick":
            for item in self.items_inventory:
                if item.name.lower() in inp:
                    game.player.inventory.append(item)
                    self.items_inventory.remove(item)
                    break
        elif words[0] == "use":
            for item in game.player.inventory:
                if item.name.lower() in inp:
                    item_to_use = item
                    break
            if item_to_use.is_weapon:
                if self.distance_to_enemies <= self.close_range:
                    if not item_to_use.range:
                        self.use_weapon(item_to_use)
                    else:
                        print("You are too close to use this.")
                else:
                    if item_to_use.range:
                        self.use_weapon(item_to_use)
                    else:
                        print("You are too far away to use this.")
            else:
                print("use in other way")
        elif words[0] == "drop":
            for item in game.player.inventory:
                if item.name.lower() in inp:
                    game.player.inventory.remove(item)
                    self.inventory_items.append(item)
                    break
        self.update_distance_to_enemies(-self.enemy_move_distance)
    
    def update_distance_to_enemies(self, change):
        self.distance_to_enemies += change
        if self.distance_to_enemies < 0:
            self.distance_to_enemies = 0
        elif self.distance_to_enemies > self.max_distance:
            self.distance_to_enemies = self.max_distance
    
    def use_weapon(self, item_to_use):
        damage_to_deal = item_to_use.damage * game.player.stats["strength"].points
        count = 0
        dead_count = 0
        if item_to_use.group:
            dead_enemies = []
            for enemy in self.enemies:
                count += 1
                if enemy.deal_damage(damage_to_deal):
                    dead_enemies.append(enemy)
            for enemy in dead_enemies:
                self.enemies.remove(enemy)
                dead_count += 1
        else:
            enemy = self.enemies[random.randint(0,len(self.enemies)-1)]
            count += 1
            if enemy.deal_damage(damage_to_deal):
                self.enemies.remove(enemy)
                dead_count += 1
        print()
        print(damage_to_deal, "damage dealt to", count, self.enemy_data["name"] + "(s).")
        print(dead_count, "enemies eliminated.")
    
    def deal_to_player(self, d):
        damage_dealt = 0
        dmg = d * (1 - game.player.stats["strength"].points / 4)
        for enemy in self.enemies:
            if random.randint(1,100) >= (game.player.stats["luck"].points / 2) * 100:
                game.player.take_damage(dmg)
                damage_dealt += dmg
        print("\nYou just received", damage_dealt, "damage.", game.player.health.health, "remaining.")
    
    def normalise_input(self, inp):
        inp = inp.strip()
        inp = inp.lower()
        new_txt = ""
        for char in inp:
            if not char.isdigit() and not char in string.punctuation:
                new_txt += char
        return new_txt
    
class enemy:
    def __init__(self, data):
        self.name = data["name"]
        self.description = data["description"]
        self.health = data["health"]
        self.range_damage = data["range_damage"]
        self.close_damage = data["close_damage"]
    
    def deal_damage(self, dmg):
        self.health -= dmg
        if self.is_dead():
            return True
        return False
    
    def is_dead(self):
        if self.health <= 0:
            return True
        return False

class weapon:
    def __init__(self, n, d, r, g):
        self.name = n
        self.damage = float(d) # float containing how much damage is done
        self.range = bool(int(r)) # boolean, True if long, False if close range
        self.group = bool(int(g)) # boolean, True if it can damage multiple enemies at once
        self.is_weapon = True

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
        self.alcohol_units = float(read_file_where(r"..\text\drinks.txt", n)[1]) # dictates how drunk the player will get after consumption
    
    def consume(self):
        print("DRINKING", self.name)

class food:
    def __init__(self, n, p):
        self.name = n
        self.price = float(p)
        self.type = "FOOD"
        self.sustinance = float(read_file_where(r"..\text\foods.txt", n)[1]) # dictates how much health a player will gain / how much drunkenness the player will lose
    
    def consume(self):
        print("EATING", self.name)

class shop_item:
    def __init__(self, n):
        self.name = n
        data = read_file_where(r"..\text\shop_items.txt", n)
        self.price = float(data[1])
        self.use = data[2]
        self.amount = float(data[3])
        self.description = data[4]
        self.num_uses = int(data[5])
        self.is_weapon = bool(int(data[6]))
        if self.is_weapon:
            self.range = bool(int(data[6]))
            self.group = bool(int(data[7]))
            self.damage = float(data[8])
    
    def buy(self):
        print("You have bought", self.name)
    
    # potential uses of items
    # REDUCE DRUNKENNES, INCREASE HEALTH, INCREASE LUCK, ...

def initialise_locations():
    locations = {}  # dictionary to store locations
    data = read_file(r"..\text\location_descriptions.txt")

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