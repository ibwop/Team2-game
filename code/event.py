import random
from file_manager import *

class Encounter():
    def __init__(self, d, a):
        self.description = d
        self.actions = a
        self.count = 0

    def create_encounters(self):
        """reads encounter data and returns a numbered dictionary of encounters"""
        encounter_data = read_file("text/encounters.txt")
        encounters_dict = {}

        for index, encounter in enumerate(encounter_data):
            description = encounter[0]
            npc = encounter[1]
            actions = encounter[2:5]
            outcomes = encounter[5:8]
            effects = encounter[8:11]

        encounters_dict[index] = {
            'description': description,
            'npc': npc,
            'actions': actions,
            'outcomes': outcomes,
            'effects': effects
        }

        return encounters_dict

    def random_encounter(self):
        """Generates a random encounter"""
        encounters = self.create_encounters()
        encounter_choice = random.choice(encounters.keys())
        
        description = encounter_choice['description']
        actions = encounter_choice['actions']
        outcomes = encounter_choice['outcomes']
        effects = encounter_choice['effects']

        action = input(description, "You can", actions[0], "or", actions[1], "or", actions[2])

        if action == action[0]:
            # consequenes for actions 1
            print(outcomes[0])
            # maybe adjust player stats
            pass
        elif action == action[1]:
            # consequences for action 2
            print(outcomes[1])
            # etc
            pass

    
    def trigger_encounter(self):
        """Random triggers encounters (20% chance)"""
        # if encounter recently triggered (past 3 turns) then 0% chance for encounter
        if self.counter > 0:
            self.counter -=1
            return False
        if random.random() > 0.2:
            self.counter = 3
            self.random_encounter()
        return False

