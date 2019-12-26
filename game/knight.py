import pyglet
import random
from game import resources, setup

class Knight():
    def __init__(self):
        self.deleting = False
        self.canRemove = False
        self.playerSprite = pyglet.sprite.Sprite(
            img=resources.player_image_left, x=random.randint(
                resources.player_image_left.width/2, setup.screen_width - resources.player_image_left.width / 2),
            y=random.randint(resources.player_image_left.height/2, setup.screen_height -
                             resources.player_image_left.height / 2),
            batch=resources.main_batch)
        self.playerSprite.velocity = random.randint(5, 9) * 50
        self.playerSprite.velocity_x, self.playerSprite.velocity_y = self.playerSprite.velocity * \
            random.choice([-1, 1]), self.playerSprite.velocity * \
            random.choice([-1, 1])

    def check_bounds(self):
        min_x = self.playerSprite.width / 2
        min_y = self.playerSprite.height / 2
        max_x = setup.screen_width - self.playerSprite.width / 2
        max_y = setup.screen_height - self.playerSprite.height / 2
        if self.playerSprite.x <= min_x and self.playerSprite.velocity_x < 0:
            self.playerSprite.velocity_x = self.playerSprite.velocity
        elif self.playerSprite.x >= max_x and self.playerSprite.velocity_x > 0:
            self.playerSprite.velocity_x = -self.playerSprite.velocity
        if self.playerSprite.y <= min_y and self.playerSprite.velocity_y < 0:
            self.playerSprite.velocity_y = self.playerSprite.velocity
        elif self.playerSprite.y >= max_y and self.playerSprite.velocity_y > 0:
            self.playerSprite.velocity_y = -self.playerSprite.velocity

    def update(self, dt):
        if not self.deleting:
            self.playerSprite.position = self.playerSprite.x + self.playerSprite.velocity_x * dt, self.playerSprite.y + self.playerSprite.velocity_y * dt
            self.check_bounds()
            
            if self.playerSprite.velocity_x > 0 and self.playerSprite.image == resources.player_image_left:
                self.playerSprite.image = resources.player_image_right
            elif self.playerSprite.velocity_x < 0 and self.playerSprite.image == resources.player_image_right:
                self.playerSprite.image = resources.player_image_left
        else:
            if self.playerSprite.opacity > 0:
                if self.playerSprite.opacity - dt*1000 < 0:
                    self.playerSprite.opacity = 0
                    self.canRemove = True
                else:
                    self.playerSprite.scale += dt
                    self.playerSprite.opacity -= dt*1000
                    self.playerSprite.color = (
                        255, 255 - dt*10000, 255 - dt*10000)
                    self.playerSprite.rotation += dt*random.randint(400, 2000)

    def draw(self):
        self.playerSprite.draw()
