from items import *
from map import *
from player import *
import string

time = [19,0]
closing_time = [1,0]
inside = False # stores whether the player is inside a building or on the street
player = Player()

def update_time(mins):
    global time
    time[0] = int(time[0])
    time[1] = int(time[1])
    time[1] += mins
    while time[1] >= 60:
        time[0] += 1
        time[1] -= 60
    while time[0] >= 24:
        time[0] -= 24

def time_to_text(t):
    text = ""
    while len(str(t[0])) < 2:
        t[0] = "0" + str(t[0])
    while len(str(t[1])) < 2:
        t[1] = "0" + str(t[1])
    return str(t[0]) + ":" + str(t[1])

def print_menu():
    print()
    print(player.current_location.name.upper())
    print()
    print(time_to_text(time))
    print()
    print(player.current_location.description)
    print()
    player.print_money()
    print()
    player.print_inventory()
    print()
    print("GO INSIDE")
    player.current_location.print_exits()

def remove_punct(text): #removes punctuation from the user input
    new_text = ""
    for char in text:
        if char not in string.punctuation:
            new_text += char
    return new_text

def take_input():    
    #take users input and make lower case
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
            global inside
            inside = True
        elif is_valid_exit(player.current_location, inp[1]):
            update_time(player.get_travel_time(inp[0])) # randomise the time taken to walk between the two locations (based on stats)
            # randomise if player encounters an NPC en route
            player.move_location(inp[1])
            print(player.current_location)
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
    global inside
    inside = False

def execute_inside(inp):
    t = player.current_location.type
    if t == "PUB":
        amount, go_outside = player.current_location.execute_inside(inp, player.money)
        player.update_money(amount)
        if go_outside:
            done_inside()
    elif t == "SHOP":
        amount, go_outside, item_bought = player.current_location.execute_inside(inp, player.money)
        if item_bought is not None:
            player.add_to_inventory(item_bought)
        player.update_money(amount)
        if go_outside:
            done_inside()

def main():
    while True:
        if not inside:
            print_menu()
            
            user_input = take_input()
            
            execute_input(user_input)
        else:
            player.current_location.go_inside()
            
            player.print_money()
            
            user_input = take_input()
            
            execute_inside(user_input)

if __name__ == "__main__":
    main()
    