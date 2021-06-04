from ursina import *
from first_person_controller import FirstPersonController
from generator import generate_world, show_world
from ursina.shaders import basic_lighting_shader
import random
app = Ursina()

world = generate_world()
player = FirstPersonController()
Sky(color=color.hex("#130310"))
number = 3
scene.fog_density = .1
scene.fog_color = color.black
print(show_world(world))

for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "#":
            if random.randint(0,8) == 1:
                Entity(model="cube", texture="wall2w.png", collider="box", position = (x*number, 0, y*number), scale = number)
            else:
                Entity(model="cube", texture="wall2.png", collider="box", position=(x * number, 0, y * number), scale=number)
        elif world[y][x] == "_":
            Entity(model="plane", scale=number, texture="floor.png", collider="mesh", position = (x*number, -number/2, y*number))
            Entity(model="plane", scale=number, texture="ceil.png", position=(x * number, number/2, y * number), rotation = (180, 0, 0))

floor_tiles = []
for y in range(len(world)):
    for x in range(len(world)):
        if world[y][x] == "_":
            floor_tiles.append([y, x])

spawn = floor_tiles[random.randint(0, len(floor_tiles)-1)]
player.y = number
player.x = spawn[1]*number
player.z = spawn[0]*number

def input(key):
    if held_keys['shift']:
        player.speed = 10
    else:
        player.speed = 5

    if key == "f":
        player.y = number

app.run()