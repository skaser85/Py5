import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

py5 = Py5()

x = 100
y = 100
xspeed = 1
yspeed = 3.3

def setup():
    py5.create_screen(640, 360)
    py5.background(255, 255, 0)

@py5.draw
def draw():
    global x
    global y
    global xspeed
    global yspeed
    
    py5.background(255, 255, 0)

    x = x + xspeed
    y = y + yspeed

    if (x > py5.width or x < 0):
        xspeed = xspeed * -1

    if(y > py5.height or y < 0):
        yspeed = yspeed * -1

    py5.fill(255, 0 ,255)
    py5.circle(x, y, 16)

setup()
draw()
