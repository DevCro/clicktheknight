import pyglet
import glooey
import random
import time
from pyglet.window import FPSDisplay, mouse


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


screen_width = 1280
screen_height = 720
knight_num = 15
show_fps = True

main_batch = pyglet.graphics.Batch()
gui_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player_image_right = pyglet.resource.image("knight.png")
center_image(player_image_right)
player_image_left = pyglet.resource.image("knight.png", flip_x=True)
center_image(player_image_left)
button_image = pyglet.resource.image("button.png")
button_image_down = pyglet.resource.image("button_down.png")
background_image = pyglet.resource.image("background.jpeg")
background_image.width = screen_width
background_image.height = screen_height


class MyWindow(pyglet.window.Window):
    def __init__(self):
        super(MyWindow, self).__init__(screen_width, screen_height,
                                       "Click The Knight", vsync=True, fullscreen=False)

        self.gui = glooey.Gui(self, batch=gui_batch)
        self.knights = []
        self.fps_display = FPSDisplay(self)
        self.gameRunning = False
        self.createGui(None)

    def createGui(self, elapsed_time):
        vbox = glooey.VBox()
        vbox.alignment = 'center'
        if(elapsed_time == None):
            vbox.add(MyButton("START GAME"))
        else:
            vbox.add(MyLabel(f"You took: {round(elapsed_time,2)}s to finish!"))
            vbox.add(MyButton("PLAY AGAIN"))

        self.gui.add(vbox)

    def startGame(self):
        self.gameRunning = True
        self.gui.clear()
        self.start_time = time.time()
        for _ in range(knight_num):
            self.knights.append(Knight())

    def finishGame(self):
        self.gameRunning = False
        elapsed_time = time.time() - self.start_time
        self.createGui(elapsed_time)

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            for knight in reversed(self.knights):
                if knight.playerSprite.x - knight.playerSprite.width / 2 < x < knight.playerSprite.x + knight.playerSprite.width / 2 and \
                        knight.playerSprite.y - knight.playerSprite.height / 2 < y < knight.playerSprite.y + knight.playerSprite.height / 2 and not \
                        knight.deleting:
                    knight.deleting = True
                    break

    def update(self, dt):
        if self.gameRunning:
            if(len(self.knights) > 0):
                for knight in self.knights:
                    knight.update(dt)
                    if knight.canRemove:
                        self.knights.remove(knight)
                        del knight
            else:
                self.finishGame()

    def on_draw(self):
        self.clear()
        background_image.blit(0, 0)
        if self.gameRunning:
            main_batch.draw()
            if show_fps:
                self.fps_display.draw()
        else:
            gui_batch.draw()


class Knight():
    def __init__(self):
        self.deleting = False
        self.canRemove = False
        self.playerSprite = pyglet.sprite.Sprite(
            img=player_image_left, x=random.randint(
                player_image_left.width/2, screen_width - player_image_left.width / 2),
            y=random.randint(player_image_left.height/2, screen_height -
                             player_image_left.height / 2),
            batch=main_batch)
        self.playerSprite.velocity = random.randint(5, 9) * 50
        self.playerSprite.velocity_x, self.playerSprite.velocity_y = self.playerSprite.velocity * \
            random.choice([-1, 1]), self.playerSprite.velocity * \
            random.choice([-1, 1])

    def check_bounds(self):
        min_x = self.playerSprite.width / 2
        min_y = self.playerSprite.height / 2
        max_x = screen_width - self.playerSprite.width / 2
        max_y = screen_height - self.playerSprite.height / 2
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
            self.playerSprite.x += self.playerSprite.velocity_x * dt
            self.playerSprite.y += self.playerSprite.velocity_y * dt
            self.check_bounds()
            
            if self.playerSprite.velocity_x > 0 and self.playerSprite.image == player_image_left:
                self.playerSprite.image = player_image_right
            elif self.playerSprite.velocity_x < 0 and self.playerSprite.image == player_image_right:
                self.playerSprite.image = player_image_left
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


class MyLabel(glooey.Label):
    custom_color = '#FFFFFF'
    custom_font_size = 20
    custom_alignment = 'center'

class MyButton(glooey.Button):
    Foreground = MyLabel

    class Base(glooey.Image):
        custom_image = button_image
    
    class Down(glooey.Image):
        custom_image = button_image_down

    def __init__(self, text):
        super().__init__(text)

    def on_click(self, widget):
        self.window.startGame()


if __name__ == '__main__':
    window = MyWindow()

    pyglet.clock.schedule_interval(window.update, 1/144.0)
    pyglet.app.run()
