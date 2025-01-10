#import pandas as pd
import arcade
import arcade.csscolor
import arcade.csscolor
import arcade.gui
import random
import os 
import cv2
import math
#import battlespace_testing.cards
#from battlespace_testing import card_data
#from cards import get_card_dictionary
import card_data

def image_size(filename):
    """Helper function to get image file size

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    sz = os.stat (filename)

    return sz.st_size

shop_window_size = (600, 800)
battle_window_size = (800, 800)
overall_window_size = (1400,1000)

TILE_SIZE = 100
tile_width = TILE_SIZE
tile_height = TILE_SIZE

# shop mats
shop_tile_width = tile_width * 1.25
shop_tile_height = tile_height * 1.25
shop_spacing_pct = 0.2
shop_spacing_vert_pct = 0.2
shop_horizontal_offset = 250
shop_vertical_offset = overall_window_size[1] - 100
shop_width = (shop_tile_width * 3) + ((shop_tile_width * shop_spacing_pct) * 4)
shop_height = (shop_tile_height + ((shop_tile_height * shop_spacing_vert_pct) * 2))

cardret = card_data.card_return()
card_dict = cardret.get_card_dictionary()
cardlist = list(card_dict)

class ShopCard(arcade.Sprite):
    
    def __init__(self, card_id):
        
        # name of shop card to spawn in with
        self.card = card_id
        
        #dictionary storing data about this unit
        card_data = card_dict[card_id]
        sprite_txt = card_data['sprite_id'] 
        self.image_file_name = f"./images/{sprite_txt}.png"

        # get size of image to automaticall rescale to size of 1 tile
        img = cv2.imread(self.image_file_name, cv2.IMREAD_UNCHANGED)
        dimensions = img.shape

        # height, width, number of channels in image
        width = img.shape[1]
        scaleval = TILE_SIZE / width
        super().__init__(self.image_file_name, scale= scaleval, hit_box_algorithm = 'None')
        
        # store details of card internally
        self.health = card_data['hp']
        self.attack = card_data['atk']
        self.max_energy = card_data['max_energy']
        self.current_energy = 0
        # position details for combat
        self.cell_id: int
        self.column: int
        self.row: int

        # add detail sprites to the card
        self.healthdisplay = arcade.create_text_sprite(text = str(self.health),start_x = 0, start_y = 0, color = arcade.csscolor.WHITE, font_size = 25,bold = True,  font_name = "Cooper Black")
        self.attackdisplay = arcade.create_text_sprite(text = str(self.attack),start_x = 0, start_y = 0, color = arcade.csscolor.WHITE, font_size = 25, bold = True, font_name = "Henney Future")
        self.energybar = arcade.SpriteSolidColor(width=TILE_SIZE, height=1, color = arcade.csscolor.DARK_GRAY)
        self.energybar.alpha = 0
        self.show_energy_bar = False

        # coordinates for hp/atk within the card
        self.HEALTHX = 0.3 * TILE_SIZE
        self.HEALTHY = 0.35 * TILE_SIZE
        self.ATTACKX = 0.3 * TILE_SIZE
        self.ATTACKY = 0.35 * TILE_SIZE

        # this is the function triggered when card activated
        self.act_function = card_data['act_function']

    def set_position_topleft(self, top, left):
        # helper function to move all the subsprites with the tile
        self.top = top
        self.left = left

        self.healthdisplay.position = (self.position[0] + self.HEALTHX , self.position[1] - self.HEALTHY) 
        self.attackdisplay.position = (self.position[0] - self.ATTACKX , self.position[1] - self.ATTACKY) 
 
    def set_position_cxy(self, position):

        #print("pos 0: ", position[0], "pos 1: ", position[1])
        #print("center x:", self.center_x, "center y: ", self.center_y)
        self.center_x = position[0]
        self.center_y = position[1]

        self.healthdisplay.position = (self.position[0] + self.HEALTHX , self.position[1] - self.HEALTHY) 
        self.attackdisplay.position = (self.position[0] - self.ATTACKX , self.position[1] - self.ATTACKY) 

        self.energybar.position = (self.position[0], self.position[1])
        self.energybar.top = self.top

    def add_to_list(self, targetlist:arcade.SpriteList):
        # helper function to add all the subsprites to the right spritelist
        self.remove_from_sprite_lists()
        self.healthdisplay.remove_from_sprite_lists()
        self.attackdisplay.remove_from_sprite_lists()

        targetlist.append(self)
        targetlist.append(self.healthdisplay)
        targetlist.append(self.attackdisplay)
        targetlist.append(self.energybar)

    def add_energy(self, energy:int, fill:bool = False):

        # add energy to the card's internal data, and adjust the cooldown indicator
        if fill == True:
            self.current_energy = self.max_energy
        else:
            self.current_energy = self.current_energy + energy

            # make sure energy doesn't go above max
            if self.current_energy > self.max_energy:
                self.current_energy = self.max_energy

        # update the energybar visual
        missing_energy = self.max_energy - self.current_energy
        if missing_energy > 0:
            self.energybar.alpha = 200
            self.energybar.height =1
            #self.energybar.height = TILE_SIZE * (missing_energy / self.max_energy)
    
    def hide_sprite(self):
        #make sprites invisible
        self.alpha = 0
        self.healthdisplay.alpha = 0
        self.attackdisplay.alpha = 0


class BoardTile(arcade.Sprite):

    def __init__(self, card_id):

        self.tile = card_id


board_tile_status = {
    "player_one": [str(x) for x in range(0,35)],
    "player_two": [str(x) for x in range(0,35)]
}

board_tile_sprites = {
    ""
}
        

class ShopView(arcade.View):

    def __init__(self, playernum: str, next_screen_view):
        super().__init__()
        self.player_id = playernum
        self.next_screen_view = next_screen_view
        # list to hold base sprites
        self.background_spritelist: arcade.SpriteList = arcade.SpriteList()
        # list to hold shop sprites
        self.shop_spritelist: arcade.SpriteList = arcade.SpriteList()
        # list to hold the tiles of the board
        self.board_spritelist: arcade.SpriteList = arcade.SpriteList()
        # list to hold the rooms actually purchased and in the players ship
        self.ship_spritelist: arcade.SpriteList = arcade.SpriteList()
        # use this for dif behavior for dragging store and regular cards
        self.holding_store_card = False

        # set gold
        self.money = 100

        # define manager
        self.manager = arcade.gui.UIManager()
        # define V-Box
        self.v_box = arcade.gui.UIBoxLayout()

        # these variables store values needed for the dragging-dropping placement of store tiles
        self.held_tile_original_position = []
        self.held_tile = []

        # add end turn button (should advance to next player window, or to combat)
        end_turn_button = arcade.gui.UIFlatButton(text="End Turn", width=200)
        self.v_box.add(end_turn_button.with_space_around(bottom=20))
        end_turn_button.on_click = self.on_advance_button

        # add upgrade button
        upgrade_button = arcade.gui.UIFlatButton(text="Upgrade Shop", width=200)
        self.v_box.add(upgrade_button.with_space_around(bottom=20))
        upgrade_button.on_click = self.on_advance_button

        # add reroll button
        reroll_button = arcade.gui.UIFlatButton(text="Reroll ($1)", width=200)
        self.v_box.add(reroll_button.with_space_around(bottom=20))
        reroll_button.on_click = self.on_reroll_button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                child=self.v_box)
        )

    def on_advance_button(self, event):
        print('button pressed', event)
        if self.next_screen_view == None:
            arcade.close_window()
        else:    
            self.window.show_view(self.next_screen_view)

    def roll_shop(self, purchasewithmoney:bool, junk = None):
        
        print("rolling with x money: ", self.money)
        # spend one gold if we have it, otherwise do nothing
        if purchasewithmoney == True:
            print('spending 1 money')

            if self.money >= 1:
                self.money = self.money -1
            else:
                return
        
        # clear existing cardlist
        self.shop_spritelist = arcade.SpriteList()

        # pick a new set of cards to display in the shop
        for i in range(1,4):

            # ADD LOGIC HERE LATER FOR SHOP TIERS AND BUYABLE CARDS
            
            # buyable card logic
            card_selection = ""
            while card_selection == "":
                
                card_selection = cardlist[random.randint(0,len(cardlist)-1)]
                card_data = card_dict[card_selection]

                if card_data['in_shop'] is False:
                    card_selection = ""
                
                #
            shop_card = ShopCard(card_selection)

            # Handle the placement of the card in the shop
            backmat_buffer = 12.5
            
            tile_vertical_position = shop_vertical_offset - (shop_spacing_vert_pct * shop_tile_height) - backmat_buffer
            x_pos_calc = (shop_horizontal_offset + (shop_spacing_pct*shop_tile_width *i) + (shop_tile_width * (i-1))) + backmat_buffer

            #shop_card.left = x_pos_calc
            #shop_card.top = tile_vertical_position
            shop_card.set_position_topleft(tile_vertical_position, x_pos_calc)

            #self.shop_spritelist.append(shop_card)
            shop_card.add_to_list(self.shop_spritelist)
        
    def on_reroll_button(self, xys):
        print("reroll button ")
        self.roll_shop(True)

    def place_card_on_board(self, card_obj, cell_id):
        # To Do: update function to include all placement details

        # record the row and column of the card internally
        card_obj.cell_id = cell_id
        card_obj.column = ((cell_id + 1) % 7)-1
        card_obj.row = math.ceil((cell_id+1) / 7)
    
        print('placed card at row: ', card_obj.row, ' and column: ', card_obj.column )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.manager.enable()

        # setup the list of "placemat" sprites
        shop = arcade.SpriteSolidColor(int(shop_width), int(shop_height), arcade.csscolor.DARK_OLIVE_GREEN )
        shop.left = shop_horizontal_offset
        shop.top = shop_vertical_offset
        self.background_spritelist.append(shop)

        tile_vertical_position = shop_vertical_offset - (shop_spacing_vert_pct * shop_tile_height)
        # build shop tile location mats
        for i in range(1,4):
            
            x_pos_calc = (shop_horizontal_offset + (shop_spacing_pct*shop_tile_width *i) + (shop_tile_width * (i-1)))
            tile = arcade.SpriteSolidColor(int(shop_tile_width), int(shop_tile_height), arcade.csscolor.LIGHT_SEA_GREEN )
            tile.left = x_pos_calc
            tile.top = tile_vertical_position
            self.background_spritelist.append(tile)

        # set up the board placement sprites
        rows = ['a','b','c','d','e']
        lanes = ['1','2','3','4','5','6','7']
        
        # place the board in relation to the shop
        board_offset_vert = shop_vertical_offset - 650
        board_offset_hor = 200

        count = 0
        for j,row in enumerate(rows):
            for k, lane in enumerate(lanes):

                # make the board alternating colors
                tilecolor = arcade.csscolor.LIGHT_GRAY
                if count % 2 == 0:
                    tilecolor = arcade.csscolor.GRAY
                count += 1

                y_pos_calc = board_offset_vert + (tile_height * j)
                x_pos_calc = (board_offset_hor +  (tile_width * k) )

                tile = arcade.SpriteSolidColor(int(tile_width), int(tile_height), tilecolor )
                tile.alpha = 100
                tile.left = x_pos_calc
                tile.top = y_pos_calc
                self.board_spritelist.append(tile)

                board_tile_status[self.player_id][count-1] = 'empty'  

        
        # create the HQ room and position it on the board
        # 1) create the card
        hq_id = "hq_1"
        hq_space_id = 17
        hq_card = ShopCard(hq_id)
        # 2) identify and hide the board tile where we will move the hq card
        # loop through background sprites with an index id, and store if we find a match
        hq_boardspace_sprite = []
        for i, sprite in enumerate(self.board_spritelist):
            if i == hq_space_id:
                hq_boardspace_sprite = sprite
        board_tile_status[self.player_id][hq_space_id] = hq_id
        # make the board tile sprite invisible so our card isn't overlapping with it
        hq_boardspace_sprite.alpha = 0

        # 3) add  hq card to the appropriate list
        hq_card.add_to_list(self.ship_spritelist)
        # 3) move card to the correct location 
        hq_card.set_position_cxy(hq_boardspace_sprite.position)

        # record card position in card object's internal data
        self.place_card_on_board(hq_card, hq_space_id)

        # fill the shop with first set of cards
        self.roll_shop(False)

    def on_hide_view(self):
        self.manager.disable()

    def try_buy_card(self, shopcard:arcade.sprite, purchasewithmoney:bool = True):

        purchase_success = False

        # add buying criteria here
        if self.money >= 3:
            # pay for card
            purchase_success = True
            self.money = self.money - 3

            # move card from shop to ship spritelist
            print(self.shop_spritelist)
            #self.shop_spritelist.pop(self.shop_spritelist.index(shopcard))
            shopcard.add_to_list(self.ship_spritelist)

            print(self.shop_spritelist)

        return purchase_success

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        
        # check if we have any ship or shop rooms selected when we click
        picked_tile_shop = arcade.get_sprites_at_point((_x, _y), self.shop_spritelist)
        picked_tile_ship = arcade.get_sprites_at_point((_x, _y), self.ship_spritelist)

        # this clause for shop tiles
        if not picked_tile_shop == [] and self.held_tile == []:
            self.held_tile_original_position = [picked_tile_shop[0].position]
            self.held_tile = picked_tile_shop
            self.holding_store_card = True

        # this clause for board tiles     
        elif not picked_tile_ship == [] and self.held_tile == []:
            self.held_tile_original_position = [picked_tile_ship[0].position]
            self.held_tile = picked_tile_ship
            self.holding_store_card = False

    def on_mouse_release(self, _x, _y, _button, _modifiers):    
        
        def returnCard():
            print("no valid loc found")
            print("going back to: ", self.held_tile_original_position[0])
            print("from: ", self.held_tile[0].position)
            self.held_tile[0].set_position_cxy(self.held_tile_original_position[0])
            self.held_tile = []
            self.holding_store_card = False
        
        # if we are holding a card, check if we have place it somewhere
        if not self.held_tile == []:
            # look for background tiles at the point of mouse release    
            board_tile_sprite = arcade.get_sprites_at_point((_x, _y), self.board_spritelist)

            # get old board tile if there is an old position
            old_board_tile_sprite = []
            #if old_position_found:
            old_board_tile_sprite = arcade.get_sprites_at_point(self.held_tile_original_position[0], self.board_spritelist)
            old_position_found =  (len(old_board_tile_sprite) > 0)

            # if there's no board tile at release site, send card back and end function
            if board_tile_sprite == []:
                print("no board tile at release location")
                returnCard()
                return
            
            # iterator to index list of board tile sprites
            count = 0
            # id number of the cell where we find a match
            cell_id = -1
            old_cell_id = -1

            # loop through background sprites with an index id, and store if we find a match
            for sprite in self.board_spritelist:
                if sprite == board_tile_sprite[0]:
                    cell_id = count
                    print(f"cell number {cell_id} identified!")
                elif old_position_found:
                    if sprite == old_board_tile_sprite[0]:
                        old_cell_id = count
                count += 1

            print("card found is: ", cell_id)
            print(board_tile_status[self.player_id][cell_id])
        
            # if we did not find a valid cell, send tile back to its shop position
            if cell_id == -1 or not board_tile_status[self.player_id][cell_id] == 'empty':
                print('card found at location')
                returnCard()
                return


            # if we did find a valid cell, check if it is empty 
            else:

                # check whether this is a card we need to buy, and if so, check if purchase is valid
                buy_success = True
                if self.holding_store_card == True:
                    buy_success = self.try_buy_card(self.held_tile[0], True)

                if buy_success == False:
                    returnCard()
                    return

                # place tile on board
                print(board_tile_status[self.player_id])
                print("placing card: ", self.held_tile[0].card, " at: ", cell_id )

                # put the string ID of the card into the player's board
                board_tile_status[self.player_id][cell_id] = self.held_tile[0].card
                # make the board tile sprite invisible so our card isn't overlapping with it
                board_tile_sprite[0].alpha = 0
                # record board position in card's internal data
                self.place_card_on_board(self.held_tile[0], cell_id)

                # reset the board tile sprite and player board at the last position
                if old_position_found:
                    old_board_tile_sprite[0].alpha = 100
                    board_tile_status[self.player_id][old_cell_id] = 'empty'

                # add one energy DEBUG
                self.held_tile[0].add_energy(1)

                # update the board tiles position and remove it from our 'holding list
                self.held_tile[0].set_position_cxy(board_tile_sprite[0].position)
                self.held_tile = []
        
    def on_mouse_motion(self, _x, _y, dx, dy):
        
        if self.held_tile == []:
            pass
        else:
            for tile in self.held_tile:
                tile.set_position_cxy((tile.center_x + dx, tile.center_y + dy))
                #tile.center_x += dx
                #tile.center_y += dy
    
    def on_draw(self):
        self.clear()

        # title the shop
        title_text = "SHOP SCREEN FOR " + self.player_id
        arcade.draw_text(title_text, overall_window_size[0]/4, 950, arcade.color.BLACK, font_size= 20, anchor_x= "left")

        # display current money
        money_text = "$" + str(self.money)
        arcade.draw_text(money_text, overall_window_size[0]/10, 700, arcade.color.BLACK, font_size= 20, anchor_x= "left")

        # display sprites
        self.manager.draw()
        self.background_spritelist.draw()
        self.shop_spritelist.draw()
        self.board_spritelist.draw()
        self.ship_spritelist.draw()


class FightView(arcade.View):

    def __init__(self, playeroneshopview, playertwoshopview):
        super().__init__()
        self.player1shop = playeroneshopview
        self.player2shop = playertwoshopview
        self.player1_board_sprites: arcade.SpriteList
        self.player2_board_sprites: arcade.SpriteList
        # spritelist for effects that appear and disapear (bullets, green activation flash)
        self.fx_spritelist = arcade.SpriteList()

        
        self.viewShown = False
        # next screen view should be player1shop view, so that cycle of playthrough can continue
        self.next_screen_view = playeroneshopview

        # these are the dictionaries that hold all fight data in one place 
        # {obj_n: {'player':int, 'row':0, 'col':1, 'sprite':sprite_from_board, 'hp':sprite_hp, 'atk': sprite_atk}}
        self.player_board_data = {}

        # tick to keep track of fight timing
        self.fight_heartbeat = 0
        # step to keep track of fight resolution
        self.fight_step = 0
        # keep track of which player is first
        self.player_order = [0,1]


        # END FIGHT BUTTON SECTION, ALL GUI
        # define manager
        self.manager = arcade.gui.UIManager()
        # define V-Box
        self.v_box = arcade.gui.UIBoxLayout()
        # add end fight button (should advance back to first player window)
        end_turn_button = arcade.gui.UIFlatButton(text="End Fight", width=200)
        self.v_box.add(end_turn_button)
        end_turn_button.on_click = self.on_advance_button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="top",
                child=self.v_box)
        )

    def on_advance_button(self, event):
        print('end fight button pressed', event)
        if self.next_screen_view == None:
            arcade.close_window()
        else:    
            self.window.show_view(self.next_screen_view)


    def build_board_objects(self):
        
        # add cards from playerboards to data structure
        for playernum, playerboard in enumerate([self.player1_board_sprites, self.player2_board_sprites]):
            for card_obj in playerboard:

                # only proceede if sprite is a shopcard
                if card_obj.__class__.__name__ != "ShopCard": 
                    continue

                # create data object to add to dictionary
                card_data = {
                    'player': playernum,
                    'row': card_obj.row,
                    'col': card_obj.column,
                    'cell_id': card_obj.cell_id,
                    'sprite_id': card_obj.card,
                    'hp': card_obj.health,
                    'atk': card_obj.attack,
                    'object': card_obj
                }

                # unique string to use as key in dictionary (mostly wont reference this)
                # format cardname_p[playernum]_c[col]_r[row]
                # i.e.: turret1_p1_c2_r1
                uq_str = card_data['sprite_id'] + \
                    '_p' + str(card_data['player']) + \
                          '_c' + str(card_data['col']) +  \
                            '_r' + str(card_data['row'])
                
                print('added uq str: ', uq_str)

                # add obj string inside obj so we can reference it later
                card_data['uq_id'] = uq_str

                # add data objects to overall game state data list
                self.player_board_data[uq_str] = card_data
           
    def on_show_view(self):
        # enable the UI of this view to be shown
        self.manager.enable()

        self.player1_board_sprites = self.player1shop.ship_spritelist
        self.player2_board_sprites = self.player2shop.ship_spritelist

        self.viewShown = True

        # rotate boards
        for tile in self.player1_board_sprites:
            # make changes to shopcards, they will move their associated sprites
            if tile.__class__.__name__ == "ShopCard":
                #print("tile type: ", tile.__class__.__name__)
                tile.set_position_cxy((tile.position[1]-75, tile.position[0] - 50))
                #print("tile start angle: ", tile.angle)
                tile.angle = -90
                #print("tile after angle: ", tile.angle)
        
        for tile in self.player2_board_sprites:
            # make changes to shopcards, they will move their associated sprites
            if tile.__class__.__name__ == "ShopCard":
                #print("tile type: ", tile.__class__.__name__)
                tile.set_position_cxy((700  + (800 - tile.position[1]), tile.position[0] - 50))
                #print("tile start angle: ", tile.angle)
                tile.angle = 90

        self.build_board_objects()

    def calculate_hit(self, attacker_sprite: ShopCard, defender_sprite: ShopCard, update_action: dict, live_board_data: dict):
        
        # should only be called when update action is a hit
      
        if attacker_sprite.attack >= defender_sprite.health:
            # room destroyed
            defender_sprite.hide_sprite()
        else:
            # update sprite health value and displayed health value
            defender_sprite.health -= attacker_sprite.attack
            defender_sprite.healthdisplay.text = str(defender_sprite.health)

            print('defendersprite new health: ', defender_sprite.health)
            print('defendersprite text sprite new health: ', defender_sprite.healthdisplay.text)

    def advance_fight(self, step = None, update_board = True):
        

        # indexes that store the current point in time of the fight resolver (given that this is a 'step' function)
        # use stored value unless (for debug) we want to see a particular step
        if step == None:
            step = self.fight_step

        print('CHECKING STEP: ', step)

        # update FX sprites from last step to disappear
        self.fx_spritelist = arcade.SpriteList()

        # check validity of board
            # board tiles sorted into "active," "destroyed," "disconnected" lists

        # get turn number

        # if first turn
        if step == 0:
            # decide and store first and second player
            first_player = random.randint(0,1)
            player_order = [first_player, 1 - first_player]
            self.player_order = player_order

            # do any start of fight effects here
            # NOT CREATED ANY ATM

        # this list stores all the attacks/heals etc. that are returned by the cards activated on this step, so they can be resolved
        board_updates = []

        # variable that tracks where in function to trigger given the input step value
        req_step = 0

        # activation stage, for each player
        for player_number in self.player_order:

            # loop through positions on board from first row moving back, left to right
            for row in range(0,5):
                for column in range(0,7):

                    # check if given row-column placement has a board tile in it to trigger
                    activated_board_obj = None
                    for name, board_obj_data in self.player_board_data.items():

                        if board_obj_data['player'] == player_number and board_obj_data['row'] == row and board_obj_data['col'] == column:
                           
                            activated_board_obj = board_obj_data
                    
                    # move to next cell if no board object found
                    if activated_board_obj == None:
                        continue

                    # each activatable tile is a new step increased by 1 from the previous
                    req_step += 1

                    # exit loop if we have passed the current step
                    if req_step > step:
                        break


                    if req_step == step:

                        # call tile's activation function 
                        print('STEP TRIGGERED FOR: ', req_step)

                        # card activation functions take in board state and return board state changes
                        # change return form of:
                        # {author_id (uq id string of activated card), 
                        #   player_id (player number),
                        #   target_id (target card uq string),
                        #  action (str of attack/heal/replace),
                        #   amount (numeric value of attacking cards attack power) }
                        returned_actions = activated_board_obj['object'].act_function(activated_board_obj, self.player_board_data)   

                        # as the object returned above may have different lengths, we loop through and append to the board_updated variable declared above
                        for action in returned_actions:
                            board_updates.append(action)

        # objects passed forward from last function:
        # [board updates], list of actions 
        # 
        #

        # After triggering the current step, this function resolves/updates the board, and animates the changes
        for update in board_updates:
            
            # get the sprite objects involved in the update
            acting_sprite = self.player_board_data[update['author_id']]['object']
            target_sprite = self.player_board_data[update['target_id']]['object']

            # animation portion
            if update['action'] == 'attack':
                
                # run the actual damage/destroying calculations
                self.calculate_hit(update_action = update, 
                                   attacker_sprite = acting_sprite, 
                                   defender_sprite = target_sprite, 
                                   live_board_data = self.player_board_data)
                

                
                ### ANIMATION SECTION
                # create a line sprite positioned at the acting sprite of length to reach the target
                for i in range(0,21):
                    
                    # we are doing a dotted line because I cannot figure out how to do cframes in this medium lol
                    #dist = arcade.get_distance_between_sprites(target_sprite,  acting_sprite)
                    linecolor = arcade.csscolor.RED
                    if update['player_id'] == 0:
                        linecolor = arcade.csscolor.BLUE
                    targetline = arcade.SpriteSolidColor(width = 7, height = 7, color = linecolor)
                    targetline.left = acting_sprite.center_x
                    targetline.top = acting_sprite.center_y

                    # calculate the angle needed to connect the line to the target sprite
                    new_x = acting_sprite.center_x - (( (acting_sprite.center_x - target_sprite.center_x)/20) * i)
                    new_y = acting_sprite.center_y - (( (acting_sprite.center_y - target_sprite.center_y)/20) * i)
                    targetline.center_x = new_x
                    targetline.center_y = new_y
                    #angle = math.atan2(y_diff, x_diff)
                    #targetline.radians =  angle

                    # add target line to FX spritelist that is wiped every step
                    self.fx_spritelist.append(targetline)

        # once all tiles and hits calculated                
        # check if tiles destroyed and update lists
        # check after attack if game won, exit if it has been


        # update fight step so next function call will trigger the next action in the fight
        self.fight_step += 1

    def on_draw(self):

        # clear view to start each tick clean
        self.clear() 

        # draw GUI elements
        self.manager.draw()

        # add 1 to internal timer (should be 20 ticks a second)
        self.fight_heartbeat += 1
        arcade.draw_text("time: " + str(self.fight_heartbeat), 200, 200, arcade.color.BLACK, font_size= 20, anchor_x= "left")
 
        # draw boards
        self.player1_board_sprites.draw()
        self.player2_board_sprites.draw()
        # draw fx
        self.fx_spritelist.draw()

        # tick speed for fight
        tickspeed = 40

        # based on tickspeed set above, advance fight when enough time has passed
        if self.fight_heartbeat % tickspeed == 0:
            self.advance_fight()
    
    def on_hide_view(self):
        
        self.manager.disable()

        # RESET EVERYTHING
        # VERY CLUNKY
        self.player1_board_sprites.clear()
        self.player2_board_sprites.clear()
        self.fx_spritelist.clear()
        self.viewShown = False
        self.player_board_data = {}
        self.fight_heartbeat = 0
        self.fight_step = 0

        self.clear()

        return super().on_hide_view()
    

def main():

    window = arcade.Window(overall_window_size[0], overall_window_size[1], 'test')
    #window = arcade.Window(overall_window_size[0], 2000, 'test')

    shop2_view = ShopView("player_two", None) 
    shop1_view = ShopView("player_one", shop2_view) 
    fight_view = FightView(shop1_view, shop2_view)

    shop2_view.next_screen_view = fight_view    
    fight_view.next_screen_view = shop1_view

    window.show_view(shop1_view)
    arcade.run()


if __name__ == '__main__':
    main()