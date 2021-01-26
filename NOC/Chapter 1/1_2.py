import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

location = Py5.create_vector(100, 100)
velocity = Py5.create_vector(2.5, 5)

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

    location.add(velocity)

    if (location.x > py5.width or location.x < 0):
        velocity.x = velocity.x * -1

    if(location.y > py5.height or location.y < 0):
        velocity.y = velocity.y * -1

    py5.fill(255, 0 ,255)
    py5.circle(location.x, location.y, 16)

setup()
draw()
