import cv2
import arcade
import math

class BulletSprite(arcade.Sprite):
    
    def __init__(self, image_txt, bullet_px_size, damage, speed, end_x, end_y, parent_frame, hit_params_to_pass, delay_amt = 0):
        
        # store parent frame and hit details so they can be processed when the bullet hits
        self.frame = parent_frame
        self.hit_params = hit_params_to_pass
        
        #store data about the bullet
        self.image_file_name = f"./images/{image_txt}.png"
        self.damage = damage
        self.speed = speed
        self.end_x = end_x
        self.end_y = end_y
        self.start_x = 0
        self.start_y = 0

        # track how long to delay before bullet shoots
        
        self.delay = delay_amt
        self.updates = 0

        # get size of image to automaticall rescale to size of 1 tile
        img = cv2.imread(self.image_file_name, cv2.IMREAD_UNCHANGED)


        # get width of image (should be a square), and use that to scale to desired bullet size
        width = img.shape[1]
        scaleval = bullet_px_size / width
        super().__init__(self.image_file_name, scale= scaleval, hit_box_algorithm = 'None')

    def on_update(self, delta_time = 1 / 60):
        
        if self.updates < self.delay:
            self.alpha = 255


        self.updates += 1
        
        return super().on_update(delta_time)
    
    def update_position(self):
        # used to move the bullet towards its end position based on current position and speed

        # current position
        curr_x = self.position[0]
        curr_y = self.position[1]   
        self.start_x = curr_x
        self.start_y = curr_y

        # Get the destination location for the bullet
        dest_x = self.end_x
        dest_y = self.end_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - curr_x
        y_diff = dest_y - curr_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

        # Angle the bullet sprite
        self.angle = math.degrees(angle)

        #print( abs(dest_x - curr_x + self.change_x) )

    def on_check(self):

        if self.updates < self.delay:
            self.position = (self.start_x, self.start_y)
        self.updates += 1

        # if distance from target is less than one step, proc hit
        if abs(self.end_x - self.position[0]) - abs(self.change_x) <= abs(self.change_x) and abs(self.end_y - self.position[1]) - abs(self.change_y) <= abs(self.change_y) :
            #print('hit triggered, updates: ', self.updates)
            
            self.frame.calculate_hit(update_action = self.hit_params['update_action'],
                                     attacker_sprite = self.hit_params['attacker_sprite'],
                                     defender_sprite = self.hit_params['defender_sprite'],
                                     live_board_data = self.hit_params['live_board_data'])
            self.kill() 
        

        return 
    


    def become_cheap_copy(self, otherBullet):
        # otherShopCard should be a ShopCard
        # copies position, health and attack from other input card
        self.position = otherBullet.position
        self.angle = otherBullet.angle
        self.damage(otherBullet.damage)
        self.speed(otherBullet.speed)
