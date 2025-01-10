#import pandas as pd
import arcade
import arcade.csscolor
import arcade.gui
import random
import os 
import math

def get_first_enemy_card_in_same_row(acting_card, boardstate):
    # function will automatically target next column over if needed

    target_col = acting_card['object'].column
    # str value of the UQ id of card to target
    returned_target = ""
    # Store enemy HQ column so we can move towards it with our aim
    enemy_hq_column = None
    
    # wrapped in a while loop until we have checked all the columns to the middle (col 3)
    while returned_target == "":
       
        # loop through board tiles to get tile with lowest row in same column
        # store lowest row
        lowest_row = 5

        for key, tile in boardstate.items():

            
            # only look for enemy tiles
            if tile['player'] == acting_card['player']:
                continue
            
            # record enemy HQ position
            if tile['sprite_id'] == "hq_1":
                enemy_hq_column = tile['col'] 

            # if we find a new closest valid target, store it
            if tile['col'] == target_col and tile['row'] < lowest_row and tile['status'] == 'alive': 

                lowest_row = tile['row']
                returned_target = key

    

        # if we didn't find in the previous column, move target column closer to the center
        if returned_target  == "":
            # if we are checking center and no HQ column, then exit and accept we have no valid target
            if target_col == enemy_hq_column:
                break
            elif target_col > enemy_hq_column:
                target_col -= 1
            elif target_col < enemy_hq_column:
                target_col += 1
    
    if returned_target == "":
        print("ERROR NO TARGET FOUND by: ", acting_card['uq_id'])
        print("FIGHT MIGHT HAVE ENDED ALREADY")
        return
    else:
        return returned_target


    # if no tile in same column, move towards middle (3)



def turret_1_activation(acting_turret, boardstate):
    # this function is for the turret_1 card
    # it detailsi how the card will fun

    # return type for activation functions ()
    targeted_card = get_first_enemy_card_in_same_row(acting_turret, boardstate)

    # change return form of list of [(target uq_id, change type ["attack", "heal", "replace"], animationID )]
    attack_dict = {'author_id': acting_turret['uq_id'], 'player_id' : acting_turret['player'],'target_id': targeted_card, 'action': 'attack', 'amount': acting_turret['object'].attack}

    return [attack_dict]




card_dict = {
    'turret_1': {
        'in_shop': True,
        'sprite_id': 'turret_1',
        'tier': 1,
        'hp': 5,
        'atk': 10,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
    },

    'turret_2': {
        'in_shop': True,
        'sprite_id': 'turret_2',
        'tier': 1,
        'hp': 5,
        'atk': 1,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']  
    },

    'hq_1': {
        'in_shop': False,
        'sprite_id': 'hq_1',
        'tier': 1,
        'hp': 8,
        'atk': 0,
        'max_energy': 3,
        'on_energy_max': [],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']  
    },

    'lightning_1': { 
        'in_shop': True,      
        'sprite_id': 'lightning_1',
        'hp': 8,
        'atk': 0,
        'max_energy': 3
    },
    'lightning_2': {    
        'in_shop': True,   
        'sprite_id': 'lightning_2',
        'hp': 8,
        'atk': 0,
        'max_energy': 2
    },
    'portal_1': {
        
        'in_shop': True,       
        'sprite_id': 'portal_1',
        'hp': 8,
        'atk': 0,
        'max_energy': 3
    },
    'tentacle_1': {  
        'in_shop': True,     
        'sprite_id': 'tentacle_1',
        'hp': 8,
        'atk': 0,
        'max_energy': 3
    },
    'tentacle_2': { 
        'in_shop': True,      
        'sprite_id': 'tentacle_2',
        'hp': 8,
        'atk': 0,
        'max_energy': 3
    }
}

class card_return():
    def __init__(self):
        pass

    def get_card_dictionary(self):
        """Dummy function to pass card data to main script

        Returns:
            dictionary: dictionary of the data needed to run cards objects 
        """


        return card_dict
    

# dummy setup to test activation functions
for item in card_dict:
    card_dict[item]['act_function'] = turret_1_activation
