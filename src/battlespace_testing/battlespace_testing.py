#import pandas as pd
import arcade
import arcade.csscolor
import arcade.gui
import random
import os 
import cv2


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
overall_window_size = (1000,1000)

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

card_dict = {
    'turret_1': {
        'in_shop': True,
        'sprite_id': 'turret_1',
        'tier': 1,
        'hp': 5,
        'atk': 1,
        'energy_max': 2,
        'on_energy_max': ['attack_function'],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']  
    },

    'turret_2': {
        'in_shop': True,
        'sprite_id': 'turret_2',
        'tier': 1,
        'hp': 5,
        'atk': 1,
        'energy_max': 2,
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
        'energy_max': 0,
        'on_energy_max': [],
        'on_place_first': ['default'],
        'on_place_any': ['default'],
        'on_moved': ['default']  
    },

    'lightning_1': {       
        'sprite_id': 'lightning_1',
        'hp': 8,
        'atk': 0
    },
    'lightning_2': {       
        'sprite_id': 'lightning_2',
        'hp': 8,
        'atk': 0
    },
    'portal_1': {       
        'sprite_id': 'portal_1',
        'hp': 8,
        'atk': 0
    },
    'tentacle_1': {       
        'sprite_id': 'tentacle_1',
        'hp': 8,
        'atk': 0
    },
    'tentacle_2': {       
        'sprite_id': 'tentacle_2',
        'hp': 8,
        'atk': 0
    }
}
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

        # add details to the card
        self.healthdisplay = arcade.create_text_sprite(text = str(self.health),start_x = 0, start_y = 0, color = arcade.csscolor.WHITE, font_size = 25,bold = True,  font_name = "Cooper Black")
        self.attackdisplay = arcade.create_text_sprite(text = str(self.attack),start_x = 0, start_y = 0, color = arcade.csscolor.WHITE, font_size = 25, bold = True, font_name = "Henney Future")

        # coordinates for hp/atk within the card
        self.HEALTHX = 0.3 * TILE_SIZE
        self.HEALTHY = 0.35 * TILE_SIZE
        self.ATTACKX = 0.3 * TILE_SIZE
        self.ATTACKY = 0.35 * TILE_SIZE

    def set_position_topleft(self, top, left):
        # helper function to move all the subsprites with the tile
        self.top = top
        self.left = left

        self.healthdisplay.position = (self.position[0] + self.HEALTHX , self.position[1] - self.HEALTHY) 
        self.attackdisplay.position = (self.position[0] - self.ATTACKX , self.position[1] - self.ATTACKY) 
 
    def set_position(self, position):
        self.center_x = position[0]
        self.center_y = position[1] 

        self.healthdisplay.position = (self.position[0] + self.HEALTHX , self.position[1] - self.HEALTHY) 
        self.attackdisplay.position = (self.position[0] - self.ATTACKX , self.position[1] - self.ATTACKY) 

    def add_to_list(self, targetlist:arcade.SpriteList):
        # helper function to add all the subsprites to the right spritelist
        self.remove_from_sprite_lists()
        self.healthdisplay.remove_from_sprite_lists()
        self.attackdisplay.remove_from_sprite_lists()

        targetlist.append(self)
        targetlist.append(self.healthdisplay)
        targetlist.append(self.attackdisplay)





    

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
        self.money = 10

        # define manager
        self.manager = arcade.gui.UIManager()
        # define V-Box
        self.v_box = arcade.gui.UIBoxLayout()


        # these variables store values needed for the dragging-dropping placement of store tiles
        self.held_tile_original_position = []
        self.held_tile = []

        # this is the table of 


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
            card_selection = ""
            card_selection = cardlist[random.randint(0,len(cardlist)-1)]
            card_data = card_dict[card_selection]
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

            
            #self.ship_spritelist[shopcard]



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
            self.held_tile[0].set_position(self.held_tile_original_position[0])
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

                # reset the board tile sprite and player board at the last position
                if old_position_found:
                    old_board_tile_sprite[0].alpha = 100
                    board_tile_status[self.player_id][old_cell_id] = 'empty'

                # update the board tiles position and remove it from our 'holding list
                self.held_tile[0].set_position(board_tile_sprite[0].position)
                self.held_tile = []
        
    def on_mouse_motion(self, _x, _y, dx, dy):
        
        if self.held_tile == []:
            pass
        else:
            for tile in self.held_tile:
                tile.set_position((tile.center_x + dx, tile.center_y + dy))
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

    def __init__(self, playeroneshop, playertwoshop):
        super().__init__()
        self.player1shop = playeroneshop
        self.player2shop = playertwoshop
        self.player1board: arcade.SpriteList
        self.player2board: arcade.SpriteList
        self.viewShown = False

    def on_show_view(self):

        self.player1board = self.player1shop.ship_spritelist
        self.player2board = self.player2shop.ship_spritelist

        self.viewShown = True


        # rotate boards
        for tile in self.player1board:
            tile.set_position((tile.position[1], tile.position[0]))
            tile.angle = 90
    
    def on_draw(self):

        self.player1board = self.player1shop.ship_spritelist
        self.player2board = self.player2shop.ship_spritelist
        
        self.clear() 

        self.player1board.draw()
        self.player2board.draw()


def main():

    window = arcade.Window(overall_window_size[0], overall_window_size[1], 'test')
    

    shop2_view = ShopView("player_two", None) 
    shop1_view = ShopView("player_one", shop2_view) 
    fight_view = FightView(shop1_view, shop2_view)

    shop2_view.next_screen_view = fight_view    
    
    window.show_view(shop1_view)
    arcade.run()


if __name__ == '__main__':
    main()