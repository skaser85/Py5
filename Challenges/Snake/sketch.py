import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from Vector import Vector
from Snake import Snake
import pygame

py5 = Py5()

scl = 20
snake = Snake(py5, scl, 200, 200)

def pick_location():
    cols = py5.floor(py5.width / scl)
    rows = py5.floor(py5.height / scl)
    global food
    food = py5.create_vector(py5.floor(py5.random_int(cols)), py5.floor(py5.random_int(rows)))
    food.mult(scl)

def setup():
    py5.create_screen(600, 600)
    py5.set_framerate(10)
    pick_location()

@py5.draw
def draw():
    py5.background(50)

    pressed_keys = py5.get_pressed_keys()

    if pressed_keys:
        if py5.KEY_UP:
            if pressed_keys[py5.UP_ARROW]:
                snake.dir(0, -1)
            elif pressed_keys[py5.DOWN_ARROW]:
                snake.dir(0, 1)
            elif pressed_keys[py5.RIGHT_ARROW]:
                snake.dir(1, 0)
            elif pressed_keys[py5.LEFT_ARROW]:
                snake.dir(-1, 0)

    if snake.eat(food):
        pick_location()
    snake.death()
    snake.update()
    snake.show()

    py5.fill(255, 0, 100)
    py5.rect(food.x, food.y, scl, scl)

setup()
draw()
