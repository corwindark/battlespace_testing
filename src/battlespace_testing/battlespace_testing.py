#import pandas as pd
import arcade

shop_window_size = (600, 800)
battle_window_size = (800, 800)

class ShopView(arcade.View):

    def on_show_view(self):

    def on_draw(self):

    def on_mouse_press(self, _x, _y, _button, _modifiers):

def main():
    


arcade.open_window(600,600, "example")

arcade.set_background_color(arcade.csscolor.SKY_BLUE)

arcade.start_render()   

arcade.draw_lrtb_rectangle_filled(200, 300, 200, 100, arcade.csscolor.GREEN)

arcade.draw_text("5/5", 250, 150, arcade.color.BLACK, 18)

arcade.finish_render()

arcade.run()





if __name__ == '__main__':
    main()