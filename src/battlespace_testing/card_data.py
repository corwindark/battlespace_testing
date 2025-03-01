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

def get_adjacent_cards_fight(acting_card, boardstate):
    # this function returns the cards which are adjacent to the acting card, in shopscreen spritelist

    # identify the position we are evaluating for adjacency.
    acting_column = acting_card['object'].column
    acting_row = acting_card['object'].row

    # save the adjacent room IDs
    returned_targets = []

    for key, object in boardstate.items():

        sprite = object['object']
        
        # only look at the card objects
        if sprite.__class__.__name__ != "ShopCard" or object['player'] != acting_card['player'] or object['status'] != "alive": 
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
            #print('found 1 ahead in column', sprite.card)
            returned_targets.append(sprite.cell_id)

    return returned_targets

def get_cards_behind_shop(acting_card, ship_spritelist):
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
        if acting_column == sprite.column and sprite.row > acting_row:
            #print('found 1 ahead in column', sprite.card)
            returned_targets.append(sprite.cell_id)

    return returned_targets



def get_card_in_front_shop(acting_card, ship_spritelist):
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
        if acting_column == sprite.column and sprite.row == (acting_row-1):
            #print('found a card ahead in column', sprite.card)

            found_card_id = sprite.uq_card_number
            returned_targets.append(found_card_id)
    
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

def get_all_enemy_cards_in_same_row(acting_card, boardstate):
    # get all the cards in the target column so a 'laser' can attack them all at once

    # get targeted card in conventional targeting
    target_card = get_first_enemy_card_in_same_row(acting_card, boardstate)
    
    # target col
    target_col = boardstate[target_card]['col']

    # record all cards
    targeted_cards = []


    # retrieve all cards behind it
    for key, tile in boardstate.items():
        
        if tile['player'] != acting_card['player'] and tile['col'] == target_col: 
            targeted_cards.append(key)

    # return list of enemy cards in the row
    return targeted_cards

def get_ally_cards_in_same_row(acting_card, boardstate):
    # returns the acting card's adjacent friendly rooms in the same row

    # records the card's uq_ids
    targeted_cards = []

    for key,tile in boardstate.items():
        
        # get all cards with same row but different column
        if tile['player'] == acting_card['player'] and tile['row'] == acting_card['row'] and tile['col'] != acting_card['col']:
            targeted_cards.append(key)
    
    return targeted_cards



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


def shield_discharger_attack(acting_turret, boardstate):
    # this card does a basic attack and grants shields to rooms in same row

    # shield amt (including shield power)
    shield_amt = 1 + acting_turret['object'].shield_power

    # first, get the basic attack data (will be returned at the end)
    attack_data = basic_attack(acting_turret, boardstate)
    
    # then, find all friendly cards in same row
    neighbor_friendly_cards = get_ally_cards_in_same_row(acting_turret, boardstate)

    for uq_id in neighbor_friendly_cards:
        boardstate[uq_id]['object'].update_shield('add', shield_amt)

    return attack_data


def laser_attack(acting_turret, boardstate):
    # this function is for the turret_1 card
    # it detailsi how the card will fun

    # return type for activation functions ()
    targeted_cards = get_all_enemy_cards_in_same_row(acting_turret, boardstate)

    attack_action_list = []

    for target in targeted_cards:
    
        # change return form of list of [(target uq_id, change type ["attack", "heal", "replace"], animationID )]
        attack_dict = {'author_id': acting_turret['uq_id'], 
                    'player_id' : acting_turret['player'],
                    'target_id': target, 
                    'action': 'attack', 
                    'amount': acting_turret['object'].attack,
                    'delay': 0}
        
        attack_action_list.append(attack_dict)

    return attack_action_list

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



#
def shield_surger_action(acting_card, boardstate):
    # give shield to a random adjacent room
    # not actually using modifier for fight buffs I think
    MODIFIER_ID = 'shield_surged_' + str(acting_card['object'].uq_card_number)

    # return type for activation functions ()
    # returns cell_ids of the rooms
    adj_rooms = get_adjacent_cards_fight(acting_card, boardstate)

    shield_amt = 2 + acting_card['object'].shield_power

    print('surger shield power: ', acting_card['object'].shield_power)
    # pick one of the cell IDs randomly
    target = 0
    if len(adj_rooms) > 0:
        target = adj_rooms[ random.randint(0, len(adj_rooms)-1) ]
    else:
        return
    
    #print("TARGET FOR SHIELD SURGER: ", target)

    # add 2 shields to the room object
    for key, object in boardstate.items():
        if object['player'] == acting_card['player'] and object['cell_id']  == target:
            object['object'].update_shield('add', shield_amt)
    
    return [None]




## position functions 
##


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


def shield_giver_position(acting_card, ship_spritelist):
    # updates attack based on the number of adjacent cards
    MODIFIER_ID = 'shield_giver_' + str(acting_card.uq_card_number)

    # get list of adjacent card IDs
    card_in_front = get_card_in_front_shop(acting_card, ship_spritelist)

    shield_to_grant = 2 + acting_card.shield_power

    for card in ship_spritelist:
        if card.__class__.__name__ != "ShopCard": 
            continue 
        
        # check if buff already applied 
        if MODIFIER_ID in card.modifiers.keys():

            #print('old shield buff found')

            # if buff already applied, remove old value 
            # get old value
            old_value = card.modifiers[MODIFIER_ID][1]
            # remove it
            card.update_shield('add', (-1)*old_value)
            # remove record from modifiers
            card.modifiers.pop(MODIFIER_ID, None)
        
        if len(card_in_front) > 0 and card.uq_card_number == card_in_front[0]:

            #print('card buffed with shield')

            # if not applied, add modifier to list, and add attack
            card.modifiers[MODIFIER_ID] = ('shield', shield_to_grant)
            card.update_shield('add', shield_to_grant) 

def shield_buffer_position(acting_card, ship_spritelist):
    # updates attack based on the number of adjacent cards
    MODIFIER_ID = 'shield_buffer_' + str(acting_card.uq_card_number)

    # get list of adjacent card IDs
    adj_cards = get_adjacent_cards(acting_card, ship_spritelist)

    shield_power = 2

    for card in ship_spritelist:
        if card.__class__.__name__ != "ShopCard": 
            continue 
        
        # check if buff already applied 
        if MODIFIER_ID in card.modifiers.keys():

            #print('old shield buff found')

            # if buff already applied, remove old value 
            # get old value
            old_value = card.modifiers[MODIFIER_ID][1]
            # remove it
            card.shield_power -= old_value
            # remove record from modifiers
            card.modifiers.pop(MODIFIER_ID, None)
        
        if card.cell_id in adj_cards:

            #print('card buffed with shield')

            # if not applied, add modifier to list, and add attack
            card.modifiers[MODIFIER_ID] = ('shield_power', shield_power)
            card.shield_power +=  shield_power


def light_spear_position(acting_card, ship_spritelist):

    #print('current attack: ', acting_card.attack, 'current shield', acting_card.shield)
    #print('modifiers: ', acting_card.modifiers)

    # grants attack if card is shielded
    MODIFIER_ID = 'shield_bonus'

    added_attack = 0
    if acting_card.shield > 0:
        added_attack = 2

    # check if buff already applied 
    if MODIFIER_ID in acting_card.modifiers.keys():

        # if buff already applied, remove old value 
        # get old value
        old_value = acting_card.modifiers[MODIFIER_ID][1]
        # remove it
        acting_card.change_stats('attack', (-1)*old_value)
        # remove record from modifiers
        acting_card.modifiers.pop(MODIFIER_ID, None)
    
    if added_attack > 0:
        # if not applied, add modifier to list, and add attack
        acting_card.modifiers[MODIFIER_ID] = ('attack', added_attack)
        acting_card.change_stats('attack', added_attack)     


def railgun_position(acting_card, ship_spritelist):
    # updates attack based on the number of adjacent cards
    MODIFIER_ID = 'railgun'

    # get list of cards in front and behind
    front_cards = get_cards_in_front_shop(acting_card, ship_spritelist)
    back_cards = get_cards_behind_shop(acting_card, ship_spritelist )

    # attack this card will have (0 for all non-back railguns)
    this_attack = 0

    # how many railguns in a row ahead of this one
    rails_ahead = 0
    rails_behind = 0


    # check which cell ids are railguns (card ID: railgun)
    for card in ship_spritelist:
        if card.__class__.__name__ != "ShopCard": 
            continue 
        
        if card.card == 'railgun' and card.cell_id in front_cards:
            rails_ahead += 1
        
    
        if card.card == 'railgun' and card.cell_id in back_cards:
            rails_behind += 1
        
    # set attack according to formula
    if rails_behind > 0:
        this_attack = 0
    elif rails_ahead > 0:
        this_attack = 2 + (6* (rails_ahead-1))


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
    acting_card.modifiers[MODIFIER_ID] = ('attack', this_attack)
    acting_card.change_stats('attack', this_attack) 



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
        'sprite_id': 'front_turret',
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
        'tier': 2,
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
        'tier': 2,
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
    },

    'shield_reinforcement': {
        'in_shop': True,
        'sprite_id': 'shield_reinforcement',
        'description': 'Gives 2 shield to card in front',
        'tier': 1,
        'hp': 6,
        'atk': 0,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'position_function': shield_giver_position
    },

    'light_spear': {
        'in_shop': True,
        'sprite_id': 'light_spear',
        'description': 'Gains +3 attack when shielded',
        'tier': 1,
        'hp': 3,
        'atk': 1,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'act_function': basic_attack,
        'position_function': light_spear_position
    },

    'shield_surger': {
        'in_shop': True,
        'sprite_id': 'shield_surger',
        'description': 'Gives +2 shield to one random adjacent room',
        'tier': 1,
        'hp': 2,
        'atk': 0,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'act_function': shield_surger_action
    },

    'railgun': {
        'in_shop': True,
        'sprite_id': 'railgun_room_v0.1',
        'description': 'Railgun: Massive attack scale when stacked',
        'tier': 3,
        'hp': 3, 
        'atk': 0,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default'],
        'act_function': laser_attack,
        'position_function': railgun_position
    },

    'shield_battery': {
        'in_shop': True,
        'sprite_id': 'shield_battery',
        'description': 'Shield battery: adjacent rooms grant +2 shields',
        'tier': 2,
        'hp': 3, 
        'atk': 0,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'position_function': shield_buffer_position
    },

    'shield_discharger': {
        'in_shop': True,
        'sprite_id': 'shield_discharger',
        'description': 'Shield discharger: give rooms on either side +1 shield on attack',
        'tier': 2,
        'hp': 2, 
        'atk': 4,
        'max_energy': 2,
        'on_energy_max': ['attack_function'],
        'act_function': shield_discharger_attack
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
