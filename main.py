from items import *
from map import *
from player import *

def print_menu():
    pass #print all the options for the user

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
