import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

x = 0
y = 0
spacing = 20

def setup():
    py5.create_screen(400, 400)
    py5.background(0)

@py5.draw
def draw():
    global x
    global y
    py5.fill(255)
    if Py5.random_float_range(0, 1) > 0.5:
        py5.line(x, y, x + spacing, y + spacing)
    else:
        py5.line(x, y + spacing, x + spacing, y)
    x += spacing
    if x > py5.width:
        x = 0
        y += spacing

setup()
draw()
