from items import *
from map import *
from player import *

time = 30 #1900
closing_time = 100

def update_time(mins):
    global time
    time += mins
    if time >= 2400:
        time -= 2400

def time_to_text(t):
    t = str(t)
    while len(t) < 4:
        t = "0" + t
    return t[0:2] + ":" + t[2::]

def print_menu():
    print()
    print(current_location.name.upper())
    print()
    print(time_to_text(time))
    print()
    print(current_location.description)
    print()

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

def main():
    while True:
        user_input = take_input()

print_menu()

locations["Primark"].print_menu()