#import pandas as pd
import arcade

shop_window_size = (600, 800)
battle_window_size = (800, 800)
overall_window_size = (1000,1000)

class ShopView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("SHOP SCRN", shop_window_size[0], shop_window_size[1] )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.clear()
        arcade.close_window()


def main():

    window = arcade.Window(overall_window_size[0], overall_window_size[1], 'test')
    shop1_view = ShopView()
    window.show_view(shop1_view)
    arcade.run()


if __name__ == '__main__':
    main()