import random
from file_manager import *
from dataclasses import dataclass

EXCLUDED_LOCATIONS = {"Central Bar", "Safe House"}

@dataclass
class EncounterData:
    description: str
    npc: str
    actions: list
    outcomes: list
    effects: list

class Encounter():
    def __init__(self):
        self.count = 0
        self.encounters = self.create_encounters()  # Store encounters once

    def create_encounters(self):
        """Reads encounter data and returns a numbered dictionary of encounters"""
        encounter_data = read_file("text/encounters.txt")
        encounters_dict = {}

        for index, encounter in enumerate(encounter_data):
            encounters_dict[index] = EncounterData(
                description=encounter[0],
                npc=encounter[1],
                actions=encounter[2:5],
                outcomes=encounter[5:8],
                effects=encounter[8:11]
            )

        return encounters_dict

    def random_encounter(self, location):
        """Generates a random encounter"""
        if location in EXCLUDED_LOCATIONS:
            return
        print(location)

        if not self.encounters:  # Check if there are any encounters left
            return

        # Choose a random encounter
        encounter_choice_key = random.choice(list(self.encounters.keys()))
        encounter_choice = self.encounters[encounter_choice_key]

        description = encounter_choice.description
        actions = encounter_choice.actions
        outcomes = encounter_choice.outcomes

        # Display the encounter
        print(f"{description}\n1) {actions[0]}\n2) {actions[1]}\n3) {actions[2]}")
        action = input("Choose an action (1-3): ")

        # Handle the player's choice
        if action == '1':
            self.handle_outcome(outcomes[0])
        elif action == '2':
            self.handle_outcome(outcomes[1])
        elif action == '3':
            self.handle_outcome(outcomes[2])
        else:
            print("Action not recognized, please retry")
        
        # Remove the encounter from the list after it has been used
        del self.encounters[encounter_choice_key]

    def handle_outcome(self, outcome):
        """Handles the outcome of a selected action"""
        print()
        print(outcome)
        print()

    def trigger_encounter(self, location):
        """Randomly triggers encounters (20% chance)"""
        if self.count > 0:
            self.count -= 1
            return False
        if random.random() < 0.3:  
            self.count = 3
            self.random_encounter(location)
        return False
