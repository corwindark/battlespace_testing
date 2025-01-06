#import pandas as pd
import arcade
import arcade.csscolor
import arcade.gui
import random
import os 

def get_first_enemy_card_in_same_row(acting_card, boardstate):
    # function will automatically target next column over if needed

    # loop through board tiles to get tile with lowest row in same column

    # if no tile in same column, move towards middle (3)



def turret_1_activation(acting_turret, boardstate):
    # this function is for the turret_1 card
    # it detailsi how the card will fun

    print('turret activation function triggered')

    tiles = 0
    for obj in boardstate:
        tiles += 1
    
    print('boardstate has ', tiles, ' tiles')
    print('triggered turret has: ', acting_turret.attack, ' attack') 

    # return type for activation functions ()


card_dict = {
    'turret_1': {
        'in_shop': True,
        'sprite_id': 'turret_1',
        'tier': 1,
        'hp': 5,
        'atk': 1,
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
