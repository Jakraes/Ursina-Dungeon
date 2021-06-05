from ursina import *
from main import player

class Torch(Entity):

    def __init__(self, i, **kwargs):
        super().__init__(**kwargs)
        number = 3
        self.torch = Entity(model="cube", texture="torch.png", position=(i[1]*number, 0, i[0]*number), scale=number, rotation = (0,0,0),
               double_sided = True)

    def update(self):
        self.torch.rotation_y = player.rotation_y