from map import *
from items import *
from file_manager import *

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

        

class stat:
    def __init__(self, n, d):
        self.name = n
        self.description = d
        self.points = 1 # initial value for each stat (users will allocate an amount of points to some stats)
    
    def inc_points(self, amount): # used if the user chooses to favour this stat
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