#import pandas as pd
import arcade

arcade.open_window(600,600, "example")

arcade.set_background_color(arcade.csscolor.SKY_BLUE)

arcade.start_render()   

arcade.draw_lrtb_rectangle_filled(200, 300, 200, 100, arcade.csscolor.GREEN)

arcade.draw_text("5/5", 250, 150, arcade.color.BLACK, 18)

arcade.finish_render()

arcade.run()