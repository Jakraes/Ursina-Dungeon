from ursina import *
from first_person_controller import FirstPersonController
from generator import generate_world, show_world
app = Ursina()

world = generate_world()
player = FirstPersonController()
Sky(color=color.hex("#130310"))
print(show_world(world))

for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "#":
            Entity(model="cube", texture="wall.png", collider="box", position = (x*3, 0, y*3), scale = 3)
        elif world[y][x] == "_":
            Entity(model="plane", scale=3, texture="floor.png", collider="mesh", position = (x*3, -3/2, y*3))
            Entity(model="plane", scale=3, texture="ceil.png", position=(x * 3, 3/2, y * 3), rotation = (180, 0, 0))

floor_tiles = []
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            floor_tiles.append([y, x])

spawn = floor_tiles[random.randint(0, len(floor_tiles)-1)]
player.y = 1
player.x = spawn[1]*3
player.z = spawn[0]*3

def input(key):
    if held_keys['shift']:
        player.speed = 10
    else:
        player.speed = 5

app.run()