import pyglet
import glooey
import random
from pyglet.window import FPSDisplay, mouse

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


screen_width = 1280
screen_height = 720
knight_num = 20
show_fps = True

main_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image("knight.png")
center_image(player_image)
background_image = pyglet.resource.image("background.jpeg")
background_image.width = screen_width
background_image.height = screen_height

class MyWindow(pyglet.window.Window):
    def __init__(self):
        super(MyWindow, self).__init__(screen_width, screen_height, "Click The Knight", vsync=True, fullscreen = False)
        self.gameRunning = False
        self.fps_display = FPSDisplay(self)
        self.knights = []
        for _ in range(knight_num):
            self.knights.append(Knight())


    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            for knight in reversed(self.knights):
                if knight.playerSprite.x - knight.playerSprite.width / 2 < x < knight.playerSprite.x + knight.playerSprite.width / 2 and \
                        knight.playerSprite.y - knight.playerSprite.height / 2 < y < knight.playerSprite.y + knight.playerSprite.height / 2 and not \
                        knight.deleting:
                    knight.deleting = True
                    break

    def update(self, dt):
        for knight in self.knights:
            knight.update(dt)
            if knight.canRemove:
                self.knights.remove(knight)
                del knight


class Knight():
    def __init__(self):
        self.deleting = False
        self.canRemove = False
        self.playerSprite = pyglet.sprite.Sprite(
            img=player_image, x=random.randint(
                player_image.width/2, screen_width - player_image.width / 2),
            y=random.randint(player_image.height/2, screen_height -
                             player_image.height / 2),
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
        else:
            if self.playerSprite.opacity > 0:
                if self.playerSprite.opacity - dt*1000 < 0:
                    self.playerSprite.opacity = 0
                    self.canRemove = True
                else:
                    self.playerSprite.scale += dt
                    self.playerSprite.opacity -= dt*1000
                    self.playerSprite.color = (255, 255 - dt*10000, 255 - dt*10000)
                    self.playerSprite.rotation += dt*random.randint(400,2000)


# Define a custom style for text.  We'll inherit the ability to render text
# from the Label widget provided by glooey, and we'll define some class
# variables to customize the text style.

class MyLabel(glooey.Label):
    custom_color = '#babdb6'
    custom_font_size = 10
    custom_alignment = 'center'

# If we want another kind of text, for example a bigger font for section
# titles, we just have to derive another class:

class MyTitle(glooey.Label):
    custom_color = '#eeeeec'
    custom_font_size = 12
    custom_alignment = 'center'
    custom_bold = True

# It's also common to style a widget with existing widgets or with new
# widgets made just for that purpose.  The button widget is a good example.
# You can give it a Foreground subclass (like MyLabel from above) to tell it
# how to style text, and Background subclasses to tell it how to style the
# different mouse rollover states:

class MyButton(glooey.Button):
    Foreground = MyLabel
    custom_alignment = 'fill'

    # More often you'd specify images for the different rollover states, but
    # we're just using colors here so you won't have to download any files
    # if you want to run this code.

    class Base(glooey.Background):
        custom_color = '#204a87'

    class Over(glooey.Background):
        custom_color = '#3465a4'

    class Down(glooey.Background):
        custom_color = '#729fcff'

    # Beyond just setting class variables in our widget subclasses, we can
    # also implement new functionality.  Here we just print a programmed
    # response when the button is clicked.

    def __init__(self, text, response):
        super().__init__(text)
        self.response = response

    def on_click(self, widget):
        print(self.response)

# Use pyglet to create a window as usual.

window = MyWindow()

# Create a Gui object, which will manage the whole widget hierarchy and
# interact with pyglet to handle events.

gui = glooey.Gui(window)

# Create a VBox container, which will arrange any widgets we give it into a
# vertical column.  Center-align it, otherwise the column will take up the
# full height of the window and put too much space between our widgets.

vbox = glooey.VBox()
vbox.alignment = 'center'

# Create a widget to pose a question to the user using the "title" text
# style,  then add it to the top of the vbox.

title = MyTitle("What...is your favorite color?")
vbox.add(title)

# Create several buttons with different answers to the above question, then
# add each one to the vbox in turn.

buttons = [
       MyButton("Blue.", "Right, off you go."),
       MyButton("Blue. No yel--", "Auuuuuuuugh!"),
       MyButton("I don't know that!", "Auuuuuuuugh!"),
]
for button in buttons:
   vbox.add(button)

# Finally, add the vbox to the GUI.  It's always best to make this the last
# step, because once a widget is attached to the GUI, updating it or any of
# its children becomes much more expensive.

gui.add(vbox)

# Run pyglet's event loop as usual.

pyglet.app.run()