#import pandas as pd
import arcade

shop_window_size = (600, 800)
battle_window_size = (800, 800)
overall_window_size = (1000,1000)

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
}


class ShopCard(arcade.Sprite):
    
    def __init__(self, card_id, scale = 1):
        
        self.card = card_id
        
        sprite_txt = card_dict[card_id]['sprite_id'] 
        self.image_file_name = f"../../../images/{sprite_txt}.png"

        super().__init__(self.image_file_name, scale, hit_box_algorithm = 'None')

class BoardTile(arcade.Sprite):

    def __init__(self, card_id):

        self.tile = card_id
        

class ShopView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("SHOP SCRN", shop_window_size[0], shop_window_size[1] )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.clear()
        arcade.close_window()

    def on_mouse_release(self, _x, _y, _button, _modifiers):    
        pass

    def on_mouse_motion(self, x, y, dx, dy)
        pass





def main():

    window = arcade.Window(overall_window_size[0], overall_window_size[1], 'test')
    shop1_view = ShopView()
    window.show_view(shop1_view)
    arcade.run()


if __name__ == '__main__':
    main()