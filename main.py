import pyglet
import glooey
import time
from game import resources, setup, knight
from pyglet.window import FPSDisplay, mouse

resources.background_image.width = setup.screen_width
resources.background_image.height = setup.screen_height

class MyWindow(pyglet.window.Window):
    def __init__(self):
        super(MyWindow, self).__init__(setup.screen_width, setup.screen_height,
                                       "Click The Knight", vsync=True, fullscreen=False)

        self.gui = glooey.Gui(self, batch=resources.gui_batch)
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
        for _ in range(setup.knight_num):
            self.knights.append(knight.Knight())

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
        resources.background_image.blit(0, 0)
        if self.gameRunning:
            resources.main_batch.draw()
            if setup.show_fps:
                self.fps_display.draw()
        else:
            resources.gui_batch.draw()


class MyLabel(glooey.Label):
    custom_color = '#FFFFFF'
    custom_font_size = 20
    custom_alignment = 'center'

class MyButton(glooey.Button):
    Foreground = MyLabel

    class Base(glooey.Image):
        custom_image = resources.button_image
    
    class Down(glooey.Image):
        custom_image = resources.button_image_down

    def __init__(self, text):
        super().__init__(text)

    def on_click(self, widget):
        self.window.startGame()


if __name__ == '__main__':
    window = MyWindow()

    pyglet.clock.schedule_interval(window.update, 1/144.0)
    pyglet.app.run()
