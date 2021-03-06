import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

def setup():
    py5.create_screen(640, 360)

@py5.draw
def draw():
    py5.background(255, 255, 255)

    mouse = py5.get_mouse_pos() # returns a Vector2
    center = py5.create_vector(py5.width/2, py5.height/2)

    mouse.sub(center)
    m = mouse.mag()
    py5.fill(0, 0, 0)
    py5.rect(0, 0, m, 10)

    py5.translate(center.x, center.y)
    py5.line(0, 0, mouse.x, mouse.y)

setup()
draw()
