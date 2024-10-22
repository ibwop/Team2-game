#from items import *
#from map import *
#from player import *
import game
game.initialise_variables()
from map import *
from items import *
from event import *
from player_class import *
import string


def update_time(mins):
    t = game.time
    t[0] = int(t[0])
    t[1] = int(t[1])
    t[1] += mins
    while t[1] >= 60:
        t[0] += 1
        t[1] -= 60
    while t[0] >= 24:
        t[0] -= 24
    if t[1] < 0:
        t[0] = 23
        t[1] += 60
    game.time = t

def time_to_text(t):
    text = ""
    while len(str(t[0])) < 2:
        t[0] = "0" + str(t[0])
    while len(str(t[1])) < 2:
        t[1] = "0" + str(t[1])
    return str(t[0]) + ":" + str(t[1])

def print_menu():
    print()
    print(game.player.current_location.name.upper())
    print()
    print(time_to_text(game.time))
    print()
    print(game.player.current_location.description)
    print()
    game.player.print_money()
    print()
    game.player.print_inventory()
    print()
    print("GO INSIDE")
    game.player.current_location.print_exits()

def remove_punct(text): #removes punctuation from the user input
    new_text = ""
    for char in text:
        if char not in string.punctuation:
            new_text += char
    return new_text

def take_input():    
    #take users input and make lower case
    if game.inside and (game.player.current_location.type == "PUB" or game.player.current_location.type == "SHOP"):
        user_input = input("What would you like to buy?\n").lower()
    else:
        user_input = input("What would you like to do?\n").lower()
    
    #remove punct and white space
    user_input = remove_punct(user_input)
    user_input = user_input.strip()
    
    #turn into list of individual words
    words = user_input.split()
    
    return words

def execute_go(inp):
    if len(inp) > 1:
        if inp[1] == "inside":
            game.inside = True
        elif is_valid_exit(game.player.current_location, inp[1]):
            update_time(game.player.get_travel_time(inp[0])) # randomise the time taken to walk between the two locations (based on stats)
            # randomise if player encounters an NPC en route
            game.player.move_location(inp[1])
            print(game.player.current_location.name)
        else:
            print("Can't go there.")
    else:
        print("Specify a location.")

def execute_input(inp):
    action_words = ["go", "take", "pick up"]
    if inp[0] in action_words:
        word = inp[0].lower()
        if word == "go" or word == "take":
            execute_go(inp)

def done_inside():
    game.inside = False

def execute_inside(inp):
    t = game.player.current_location.type
    if t == "PUB":
        amount, go_outside = game.player.current_location.execute_inside(inp, game.player.money)
        game.player.update_money(amount)
        if go_outside:
            done_inside()
    elif t == "SHOP":
        amount, go_outside, item_bought = game.player.current_location.execute_inside(inp, game.player.money)
        if item_bought is not None:
            game.player.add_to_inventory(item_bought)
        game.player.update_money(amount)
        if go_outside:
            done_inside()
            

def main():
    while True:
        if not game.inside:
            e = Encounter()
            if e.trigger_encounter(game.player.current_location):
                e.trigger_encounter(game.player.current_location)
            else:
                print_menu()
            
            user_input = take_input()
            
            execute_input(user_input)
        else:
            game.player.current_location.go_inside()
            
            game.player.print_money()
            
            user_input = take_input()
            
            execute_inside(user_input)

if __name__ == "__main__":
    main()
    