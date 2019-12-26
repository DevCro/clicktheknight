import pyglet

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

main_batch = pyglet.graphics.Batch()
gui_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

player_image_right = pyglet.resource.image("knight.png")
center_image(player_image_right)
player_image_left = pyglet.resource.image("knight.png", flip_x=True)
center_image(player_image_left)
button_image = pyglet.resource.image("button.png")
button_image_down = pyglet.resource.image("button_down.png")
background_image = pyglet.resource.image("background.jpeg")