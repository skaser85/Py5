import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from ship import Ship
from flower import Flower
from drop import Drop
py5 = Py5()

ship = None
flowers = []
drops = []

def setup():
    global ship
    py5.create_screen(600, 400)
    ship = Ship(py5)
    y = -300
    for i in range(5):
        flowers.append([])
        for k in range(6):
            flowers[i].append(Flower(py5, i*80+80, y+(k*80+80)))
    py5.set_framerate(10)

@py5.draw
def draw():
    py5.background(51)

    ship.show()

    for drop in drops:
        drop.show()
        drop.move()
        for flower_row in flowers:
            for flower in flower_row:
                if drop.hits(flower):
                    flower_row.remove(flower)
                    drop.evaporate()

    for drop in reversed(drops):
        if drop.to_delete:
            drops.remove(drop)

    for flower_row in flowers:
        for flower in flower_row:
            flower.update()
            flower.show()

    keys = py5.get_pressed_keys()

    if len(keys) > 0:
        if keys[py5.LEFT_ARROW]:
            ship.move(-1)
        elif keys[py5.RIGHT_ARROW]:
            ship.move(1)
        if py5.KEY_UP:
            if keys[py5.SPACE]:
                drops.append(Drop(py5, ship.x-(ship.size/2), py5.height))

setup()
draw()
