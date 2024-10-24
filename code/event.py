import random
from enum import Enum
from dataclasses import dataclass
from file_manager import read_file  # Assuming you have this function
from map import *

EXCLUDED_LOCATIONS = {"Central Bar", "Safe House"}

class ActionEnum(Enum):
    ACTION_1 = 0
    ACTION_2 = 1
    ACTION_3 = 2

@dataclass
class EncounterData:
    description: str
    npc: str
    actions: list
    outcomes: list
    effects: list

class EncounterManager:
    def __init__(self):
        self.encounters = self._load_encounters()
        self.cooldown_count = 0

    def _load_encounters(self):
        """Load and parse encounter data from file."""
        raw_data = read_file(r"..\text\encounters.txt")
        encounters_dict = {}

        for index, encounter in enumerate(raw_data):
            try:
                encounters_dict[index] = EncounterData(
                    description=encounter[0],
                    npc=encounter[1],
                    actions=encounter[2:5],
                    outcomes=encounter[5:8],
                    effects=encounter[8:11]
                )
            except (IndexError, ValueError) as e:
                print(f"Skipping encounter {index} due to error: {e}")

        return encounters_dict

    def can_trigger_encounter(self, location):
        """Checks if an encounter can be triggered based on location and cooldown."""
        if location in EXCLUDED_LOCATIONS:
            return False
        if self.cooldown_count > 0:
            self.cooldown_count -= 1
            return False
        return random.random() < 0.4

    def trigger_random_encounter(self, location, game):
        """Triggers a random encounter if conditions are met."""
        if not self.can_trigger_encounter(location):
            return False
        
        self.cooldown_count = 3
        encounter_key = random.choice(list(self.encounters.keys()))
        encounter = self.encounters.pop(encounter_key)

        print(f"Encounter: {encounter.description}")
        self.display_actions(encounter)
        player_choice = self.get_player_action()

        self.process_outcome(encounter, player_choice, game)
        return True

    def display_actions(self, encounter):
        """Displays available actions for the encounter."""
        for i, action in enumerate(encounter.actions, start=1):
            print(f"{i}) {action}")

    def get_player_action(self):
        """Gets a valid player action input."""
        while True:
            choice = input("Choose an action (1-3): ")
            if choice in {'1', '2', '3'}:
                return ActionEnum(int(choice) - 1)
            print("Invalid input. Please choose a valid action.")

    def process_outcome(self, encounter, player_choice, game):
        """Processes the chosen action's outcome and effect."""
        outcome = encounter.outcomes[player_choice.value]  
        print()
        print(f"{outcome}")
        print()

        # Check if there are enough effects for the player choice
        if len(encounter.effects) > player_choice.value:
            effect = encounter.effects[player_choice.value]  
            if effect and effect != "none":  # Apply effect only if it's not empty or "none"
                self.apply_effect(effect, game)


    def apply_effect(self, effect, game):
        """Applies the effect from the encounter."""
        # Split effect string into components
        effect_parts = effect.split()
        effect_name = effect_parts[0]

        # Apply different effects based on the effect type
        if effect_name == "adjust_stat":

            stat_name = effect_parts[1]
            sign = effect_parts[2]
            amount = float(effect_parts[3])

            current_amount = game.player.stats[stat_name].points
            if current_amount + amount > 1:
                return
            
            game.player.adjust_stat(stat_name, amount)
            print(f'Your {stat_name} has been increased by {amount} points, new value: {game.player.stats[stat_name].points}')

        elif effect_name == "add_to_inv":
            # Join parts of the effect to get the item name
            item_name = " ".join(effect_parts[1:]).rstrip()
            
            # Check if the item name exists in the items_list dictionary
            if item_name in game.items_list:
                game.player.add_to_inventory(game.items_list[item_name])
            else:
                print(game.items_list)
                print(f"Item {item_name} not found in game item list.")

        elif effect_name == "adjust_money":
            sign = effect_parts[1]
            amount = int(effect_parts[2])
            game.player.update_money(amount if sign == "+" else -amount)
            print(f"You gained £{amount}. Your new balance is {game.player.money}")

        elif effect_name == "adjust_health":
            current_health = game.player.health.health
            sign = effect_parts[1]
            amount = int(effect_parts[2])
            if current_amount + amount > 100:
                print("Your health is at it's maximum value")
            game.player.health.adjust_health(amount if sign == "+" else -amount)
            if sign == "+":
                print(f"You have gained {amount} health, your new health is {game.player.health.health}")
            elif sign == "-":
                print(f"You have lost {amount} health, your new health is {game.player.health.health}")

        else:
            print(f"Unrecognized effect: {effect}")

    def _start_fight(self, game):
        c = combat(game.player.current_location)
        
       
