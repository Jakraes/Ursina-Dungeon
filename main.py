from ursina import *
from first_person_controller import FirstPersonController
from generator import generate_world, show_world
import random

app = Ursina()

# ---------------------------------------------------------------#

world = generate_world()
player = FirstPersonController()
Sky(color=color.hex("#130310"))
number = 3
scene.fog_density = .1
scene.fog_color = color.black
wallwater = Entity()
wall = Entity()
floor = Entity()
ceil = Entity()
print(show_world(world))

# ---------------------------------------------------------------#
torch_walls = []
torch = Entity()
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            area = [world[y-1][x], world[y][x-1], world[y][x+1], world[y+1][x]]
            amount = 0
            for i in area:
                if i == "#":
                    amount += 1
            if amount == 1 or amount == 3:
                torch_walls.append([y,x])
for i in torch_walls:
    if random.randint(0,10) == 5:
        Entity(model="cube", texture="torch.png", position=(i[1]*number, 0, i[0]*number), scale=number, rotation = (0,0,0),
               double_sided = True, parent = torch)
# ---------------------------------------------------------------#
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
# ---------------------------------------------------------------#

floor_tiles = []
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            floor_tiles.append([y, x])

spawn = floor_tiles[random.randint(0, len(floor_tiles) - 1)]

player.y = number
player.x = spawn[1] * number
player.z = spawn[0] * number

# ---------------------------------------------------------------#


def input(key):
    if held_keys['shift']:
        player.speed = 10
    else:
        player.speed = 5

    if key == "f":
        player.y = number

def update():
    torch.look_at((player.world_x, 0, player.world_z), axis="forward")

app.run()
