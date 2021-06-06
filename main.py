from ursina import *
from first_person_controller import FirstPersonController
from generator import generate_world, show_world
import random


class Goblin(Entity):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self):
        origin = self.world_position
        hit_info = raycast(origin, direction=(0, -1, 0), distance=1, debug=True)
        if not hit_info.hit:
            self.y -= 0.1


app = Ursina()

# ---------------------------------------------------------------#

Audio("cave.mp3", loop=True, autoplay=True, volume=0.1)
world = generate_world()
player = FirstPersonController()
player.cursor.double_sided = True
Sky(color=color.hex("#130310"))
number = 3
scene.fog_density = .1
scene.fog_color = color.black
wallwater = Entity()
wall = Entity()
floor = Entity()
ceil = Entity()
enemies = Entity()
window.vsync = 100
window.borderless = False
window.exit_button.disable()
window.fullscreen = False
window.top = Vec2(0, 0)
print(show_world(world))

# ---------------------------------------------------------------#

torch_walls = []
torch = Entity()
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            area = [world[y - 1][x], world[y][x - 1], world[y][x + 1], world[y + 1][x]]
            amount = 0
            for i in area:
                if i == "#":
                    amount += 1
            if amount == 1 or amount == 3:
                torch_walls.append([y, x])
for i in torch_walls:
    if random.randint(0, 10) == 5:
        Entity(model="plane", texture="torch.png", position=(i[1] * number, 0, i[0] * number), scale=number,
               rotation=(-90, 0, 0), double_sided=True, parent=torch)

for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "#":
            if random.randint(0, 8) == 1:
                Entity(model="cube", texture="wall2w.png", collider="box", position=(x * number, 0, y * number),
                       scale=number, parent=wallwater)
            else:
                Entity(model="cube", texture="wall2.png", collider="box", position=(x * number, 0, y * number),
                       scale=number, parent=wall)
        elif world[y][x] == "_":
            Entity(model="plane", scale=number, texture="floor.png", collider="mesh",
                   position=(x * number, -number / 2, y * number), parent=floor)
            Entity(model="plane", scale=number, texture="ceil.png", position=(x * number, number / 2, y * number),
                   rotation=(180, 0, 0), parent=ceil)

wallwater.combine()
wall.combine()
floor.combine()
ceil.combine()
wallwater.collider = "mesh"
wallwater.texture = "wall2w.png"
wall.collider = "mesh"
wall.texture = "wall2.png"
floor.collider = "mesh"
floor.texture = "floor.png"
ceil.texture = "ceil.png"

floor_tiles = []
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            floor_tiles.append([y, x])

spawn = floor_tiles[random.randint(0, len(floor_tiles) - 1)]

player.y = number
player.x = spawn[1] * number
player.z = spawn[0] * number

for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_" and random.randint(0, 15) == 9:
            Goblin(model="cube", color=color.green, position=(x * number, 3, y * number), parent=enemies)
enemies.combine()
enemies.color = color.green
enemies.collider = "mesh"
print(enemies.children)
print(len(enemies.children))


# ---------------------------------------------------------------#


def input(key):
    if held_keys['shift']:
        player.speed = 10
    else:
        player.speed = 5

    if key == "f":
        player.y = number

    if key == "g":
        if mouse.locked:
            mouse.locked = False
        else:
            mouse.locked = True


def update():
    if held_keys["space"] == 1:
        player.y += 1
    for c in torch.children:
        if distance(c, player) < number * 15:
            c.enabled = True
            c.rotation_y = player.rotation_y
        else:
            c.enabled = False


app.run()
