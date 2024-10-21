from map import *
from items import *
from file_manager import *
import random

class Health:
    def __init__(self):
        self.health = 100 # default value
        self.attacks = self.load_attacks()

    def adjust_health(self, amount):
        self.health += amount

    def load_attacks(self):
        attacks_data = read_file("attacks.txt")  
        attacks = {}

        for attack_info in attacks_data:
            if len(attack_info) == 2:  # Ensure there are exactly two parts
                name = attack_info[0].strip()  # Get the attack name
                damage = attack_info[1].strip()  # Get the damage amount
                attacks[name] = int(damage)  # Store in dictionary
                
        return attacks
    
    def recieve_attack(self, attack_name = None):
        # Check attack exists
        if attack_name not in self.attacks:
            raise KeyError("Attack not recognised")
        
        # Get damage amount of attack
        damage_amount = self.attacks.get(attack_name)

        # Decrement health by damage
        self.adjust_health(-damage_amount)

        # Print attack message to menu
        print(f"You have been {attack_name} for {damage_amount} damage. Your health is now {self.health}")
        
class stat: # float between 0 and 1, used as a multiplier in calculations
    def __init__(self, n, d, sv):
        self.name = n
        self.description = d
        self.points = float(sv) # initial value for each stat (users will allocate an amount of points to some stats)
    
    def inc_points(self, amount): # used if the user chooses to favour this stat
        self.points += amount
        if self.points > 1:
            self.points = 1
        elif self.points < 0.01:
            self.points = 0.01

class Player:
    def __init__(self):
        self.health = Health()
        self.stats = self.initialise_stats()
        self.current_location = locations["Central Bar"]  # Starting location
        self.inventory = [items_list["Rubber Chicken"]]  # Starting inventory
        self.money = 20
        self.available_points = 1

    def initialise_stats(self):
        data = read_file("stats_descriptions.txt")
        stats = {}
        for line in data:
            stats[line[0]] = stat(line[0], line[1], line[2])
        return stats

    def allocate_points(self):
        # while there are points available
        while self.available_points > 0:
            print(f"You have {self.available_points} left to allocate")
            # loop through stats, print name and points
            for stat_name, stat_obj in self.stats.items():
                print(f"{stat_name}: {stat_obj.points}")
            # print a clear line
            print()
            # get desired stat to increase
            chosen_stat = input("Which stat would you like to increase?").lower()
            # validate that stat exists
            if chosen_stat not in self.stats.keys():
                print("Invalid stat")
                continue
            # get the amount to increment (catch non float input)
            try:
                increment = float(input("How many points would you like to add?"))
            except ValueError: 
                print("Please enter a valid number for the increment.")
                continue                  
            # if there are enough points, run increment
            if increment <= self.available_points:
                self.stats[chosen_stat].inc_points(increment)
                self.available_points -= increment
                print(f"{chosen_stat} successfully incremented by {increment}, new value is {self.stats[chosen_stat].points}")
            # otherwise, print error message and let user retry
            else:
                print("You don't have enough points to increase the stat by that much")
                continue


    def add_to_inventory(self, item):
        if item not in items_list:
            if self.current_location.type == "SHOP":
                self.inventory.append(item)
            else:
                raise KeyError("Item doesn't exist")
        else:
            self.inventory.append(items_list[item])
            print(f"{item} has been added to your inventory.")
    
    def print_inventory(self):
        print("You have:")
        for item in self.inventory:
            print(item.name)
    
    def update_money(self, amount):
        self.money += amount
    
    def print_money(self):
        print("You have: £" + str(self.money))
    
    def move_location(self, direction):
    #check if the direction is valid and exists in the current location's exits
        if direction in self.current_location.exits:
            new_location_name = self.current_location.exits[direction]
            self.current_location = locations[new_location_name]
            print(f"You have moved to {self.current_location.name}.")
        else:
             print(f"You can't go {direction} from here.")

    
    def get_travel_time(self, action_word):
        if action_word == "take":
            delay_time = 0
            if random.randint(1,100) > 100 * self.stats["luck"].points: # there will be a delay
                delay_time = random.randint(1,10)
                print("Your train was delayed by", delay_time, "minutes.")
            return 4 + delay_time # 4 mins is the normal train time
        else:
            walk_time = random.uniform(3,5) * self.stats["drunkenness"].points - random.uniform(0,2) * self.stats["health"].points - random.uniform(0,1) * self.stats["strength"].points
            if walk_time > 1:
                walk_time = 1
            elif walk_time < 0.1:
                walk_time = 0.1
            walk_time = round(walk_time * 15)
            print("The walk took you", walk_time, "minutes.")
            return walk_time