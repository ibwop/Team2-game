import random

def initialise_variables():
    
    import items
    
    global items_list
    items_list = items.initialise_items()
    
    import map
    
    global locations
    locations = map.initialise_locations()
    
    import player_class
    
    global time
    time = [19,0]
    global closing_time
    closing_time = [1,0]
    global inside
    inside = False # stores whether the player is inside a building or on the street
    global player
    player = player_class.Player()
