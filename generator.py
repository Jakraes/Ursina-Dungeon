import random
import math
import copy

room_center_coords = []

def create_blank_world(size_x=25, size_y=25, character="#"):
    world = []
    for line in range(size_y):
        world.append([])
        world[line] = size_x * [character]
    return world


def add_room(world, amount):
    for i in range(amount):
        coords = [random.randint(0, len(world) - 1), random.randint(0, len(world) - 1)]
        size = [random.randint(3, 5), random.randint(3, 5)]
        room_center_coords.append([coords[0]+math.floor(size[0]/2), coords[1]+math.floor(size[1]/2)])
        for y in range(size[0]):
            for x in range(size[1]):
                try:
                    world[coords[0]+y][coords[1]+x] = "_"
                except IndexError:
                    pass

def coord_sorter():
    indexlist = []
    for i in range(len(room_center_coords)):
        distance = math.sqrt(((room_center_coords[i][0]) ** 2) + (
                    (room_center_coords[i][1]) ** 2))
        indexlist.append(distance)
    indexlist.sort()
    lastlist=[]
    for x in range(len(indexlist)):
        lastlist.append(0)
    for i in range(len(room_center_coords)):
        item = room_center_coords[i]
        for j in range(len(room_center_coords)):
            distance = math.sqrt(((item[0]) ** 2) + ((item[1]) ** 2))
            if distance == indexlist[j]:
                lastlist[j] = item
    for i in range(len(room_center_coords)):
        room_center_coords[i] = lastlist[i]


def add_corridors(world, radius = 18):
    coord_sorter()
    for i in range(len(room_center_coords)):
        for j in range(len(room_center_coords)):
            distance = math.sqrt(((room_center_coords[j][0]-room_center_coords[i][0])**2) + ((room_center_coords[j][1]-room_center_coords[i][1])**2))
            if distance <= radius and j > i:
                yDif = room_center_coords[j][0]-room_center_coords[i][0]
                xDif = room_center_coords[j][1]-room_center_coords[i][1]
                y = 0
                x = 0
                if random.randint(0,1) == 1:
                    for x in range(xDif):
                        try:
                            world[room_center_coords[i][0]][room_center_coords[i][1]+x] = "_"
                        except IndexError:
                            pass
                    for y in range(yDif):
                        try:
                            world[room_center_coords[i][0]+y][room_center_coords[i][1]+x] = "_"
                        except IndexError:
                            pass
                else:
                    for y in range(yDif):
                        try:
                            world[room_center_coords[i][0]+y][room_center_coords[i][1]] = "_"
                        except IndexError:
                            pass
                    for x in range(xDif):
                        try:
                            world[room_center_coords[i][0]+y][room_center_coords[i][1]+x] = "_"
                        except IndexError:
                            pass


def filter_world(world):
    for y in range(len(world)):
        for x in range(len(world)):
            if y == 0 or y == len(world)-1 or x == 0 or x == len(world)-1:
                world[y][x] = "#"
    big_world = create_blank_world(len(world)+2, len(world)+2, "#")
    for y in range(len(world)):
        for x in range(len(world)):
            big_world[y+1][x+1] = world[y][x]
    for y in range(len(world)):
        for x in range(len(world)):
            area = [big_world[y][x], big_world[y][x+1], big_world[y][x+2],
                    big_world[y+1][x], big_world[y+1][x+2],
                    big_world[y+2][x], big_world[y+2][x+1], big_world[y+2][x+2]]
            if "_" not in area:
                world[y][x] = "."


def show_world(world):
    """
    Shows the world parameter in the form a string instead of a list, being separated by line breaks (\n)
    """
    rendered_world = ""
    for line in range(len(world)):
        rendered_world += ''.join(world[line])
        rendered_world += "\n"
    rendered_world = rendered_world.strip()
    return rendered_world


def generate_world():
    world = create_blank_world()
    add_room(world,7)
    add_corridors(world)
    filter_world(world)
    return world