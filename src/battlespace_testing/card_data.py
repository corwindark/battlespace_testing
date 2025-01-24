#import pandas as pd
import arcade
import arcade.csscolor
import arcade.gui
import random
import os 
import math

def get_adjacent_cards(acting_card, ship_spritelist):
    # this function returns the cards which are adjacent to the acting card, in shopscreen spritelist

    # identify the position we are evaluating for adjacency.
    acting_column = acting_card.column
    acting_row = acting_card.row

    # save the adjacent room IDs
    returned_targets = []

    for sprite in ship_spritelist:

        # only look at the card objects
        if sprite.__class__.__name__ != "ShopCard": 
            continue 
        
        # if row or column is 1 off, and other dimension the same, then it is an adjacent card
        if abs(acting_column - sprite.column) == 1 and (acting_row - sprite.row) == 0:
            returned_targets.append(sprite.cell_id)
        elif (acting_column - sprite.column) == 0 and abs(acting_row - sprite.row) == 1:
            returned_targets.append(sprite.cell_id)
    
    return returned_targets

def get_cards_in_front_shop(acting_card, ship_spritelist):
    # this function returns all allied cards in front of the acting card in the column

    # identify the position we are evaluating
    acting_column = acting_card.column
    acting_row = acting_card.row

    # save the adjacent room IDs
    returned_targets = []

    for sprite in ship_spritelist:

        # only look at the card objects
        if sprite.__class__.__name__ != "ShopCard": 
            continue 
        
        # if row or column is 1 off, and other dimension the same, then it is an adjacent card
        if acting_column == sprite.column and sprite.row < acting_row:
            print('found 1 ahead in column', sprite.card)
            returned_targets.append(sprite.cell_id)
    
    return returned_targets




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



def basic_attack(acting_turret, boardstate):
    # this function is for the turret_1 card
    # it detailsi how the card will fun

    # return type for activation functions ()
    targeted_card = get_first_enemy_card_in_same_row(acting_turret, boardstate)

    # change return form of list of [(target uq_id, change type ["attack", "heal", "replace"], animationID )]
    attack_dict = {'author_id': acting_turret['uq_id'], 
                   'player_id' : acting_turret['player'],
                   'target_id': targeted_card, 
                   'action': 'attack', 
                   'amount': acting_turret['object'].attack,
                   'delay': 0}

    return [attack_dict]

def attack_twice(acting_turret, boardstate):
    # this function is for the turret_1 card
    # it detailsi how the card will fun

    # return type for activation functions ()
    targeted_card = get_first_enemy_card_in_same_row(acting_turret, boardstate)

    # change return form of list of [(target uq_id, change type ["attack", "heal", "replace"], animationID )]
    attack_1 = {'author_id': acting_turret['uq_id'], 
                    'player_id' : acting_turret['player'],
                    'target_id': targeted_card, 
                    'action': 'attack', 
                    'amount': acting_turret['object'].attack,
                    'delay': 0}
    
    attack_2 = {'author_id': acting_turret['uq_id'], 
                    'player_id' : acting_turret['player'],
                    'target_id': targeted_card, 
                    'action': 'attack', 
                    'amount': acting_turret['object'].attack,
                    'delay': 10}

    return [attack_1, attack_2]


def forward_turret_position(acting_card, ship_spritelist):
    # updates attack based on the number of adjacent cards
    MODIFIER_ID = 'front_bonus'

    # get list of adjacent card IDs
    front_cards = get_cards_in_front_shop(acting_card, ship_spritelist)

    # 2 attack per empty adjacent space
    added_attack = 2
    if len(front_cards) > 0:
        added_attack = 0

    # check if buff already applied 
    if MODIFIER_ID in acting_card.modifiers.keys():
        # if buff already applied, remove old value 
        # get old value
        old_value = acting_card.modifiers[MODIFIER_ID][1]
        # remove it
        acting_card.change_stats('attack', (-1)*old_value)
        # remove record from modifiers
        acting_card.modifiers.pop(MODIFIER_ID, None)
        
    # if not applied, add modifier to list, and add attack
    acting_card.modifiers[MODIFIER_ID] = ('attack', added_attack)
    acting_card.change_stats('attack', added_attack) 



def void_collector_position(acting_card, ship_spritelist):
    # updates attack based on the number of adjacent cards
    MODIFIER_ID = 'void_bonus'

    # get list of adjacent card IDs
    adj_cards = get_adjacent_cards(acting_card, ship_spritelist)

    # 2 attack per empty adjacent space
    added_attack = (4 - len(adj_cards)) * 2

    # check if buff already applied 
    if MODIFIER_ID in acting_card.modifiers.keys():
        # if buff already applied, remove old value 
        # get old value
        old_value = acting_card.modifiers[MODIFIER_ID][1]
        # remove it
        acting_card.change_stats('attack', (-1)*old_value)
        # remove record from modifiers
        acting_card.modifiers.pop(MODIFIER_ID, None)
        
    # if not applied, add modifier to list, and add attack
    acting_card.modifiers[MODIFIER_ID] = ('attack', added_attack)
    acting_card.change_stats('attack', added_attack) 




    


card_dict = {

    # hq rooms for both players
    'hq_1': {
        'in_shop': False,
        'sprite_id': 'hq_1',
        'description': 'HQ room, keep it alive',
        'tier': 1,
        'hp': 8,
        'atk': 0,
        'max_energy': 3,
        'on_energy_max': [],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']  
    },    
    
    # basic tier1 turret 2/4
    'turret_1': {
        'in_shop': True,
        'sprite_id': 'turret_1',
        'description': 'Regular turret, shoots once',
        'tier': 1,
        'hp': 4, 
        'atk': 2,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
        'act_function': basic_attack
    },

    # turret that gains 2 attack in front
    'forward_turret': {
        'in_shop': True,
        'sprite_id': 'railgun_room_v0.1',
        'description': 'Front turret, +2 atk if in front',
        'tier': 1,
        'hp': 3, 
        'atk': 1,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
        'act_function': basic_attack,
        'position_function': forward_turret_position
    },

    # void turret that gains attack from empty rooms
    'void_turret': {
        'in_shop': True,
        'sprite_id': 'void_collector',
        'description': 'Void turret, +2 atk per adjacent empty tile',
        'tier': 1,
        'hp': 5,
        'atk': 1,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
        'position_function': void_collector_position,
        'act_function': basic_attack
    },

    # shoots twice
    'repeater_turret': {
        'in_shop': True,
        'sprite_id': 'turret_2',
        'description': 'Repeater, shoots twice',
        'tier': 1,
        'hp': 3,
        'atk': 1,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
        'act_function': attack_twice
    },
    
    # barrier wall, 0/6 stats, for tanking
    'barrier_wall': {
        'in_shop': True,
        'sprite_id': 'tentacle_3',
        'description': 'Barrier, no ability, absorbs damage',
        'tier': 1,
        'hp': 6,
        'atk': 0,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']
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
#for item in card_dict:
#    card_dict[item]['act_function'] = turret_1_activation
