import cv2
import arcade


class BulletSprite(arcade.Sprite):
    
    def __init__(self, image_txt, bullet_px_size, damage, speed, end_x, end_y):
        
        
        #store data about the bullet
        self.image_file_name = f"./images/{image_txt}.png"
        self.damage = damage
        self.speed = speed
        self.end_x = end_x
        self.end_y = end_y

        # get size of image to automaticall rescale to size of 1 tile
        img = cv2.imread(self.image_file_name, cv2.IMREAD_UNCHANGED)


        # get width of image (should be a square), and use that to scale to desired bullet size
        width = img.shape[1]
        scaleval = bullet_px_size / width
        super().__init__(self.image_file_name, scale= scaleval, hit_box_algorithm = 'None')


    def get_next_position(self):
        # used to move the bullet towards its end position based on current position and speed

        curr_x = self.position[0]
        curr_y = self.position[1]
        


    def become_cheap_copy(self, otherBullet):
        # otherShopCard should be a ShopCard
        # copies position, health and attack from other input card
        self.position(otherBullet.position)
        self.angle = otherBullet.angle
        self.damage(otherBullet.damage)
        self.speed(otherBullet.speed)
