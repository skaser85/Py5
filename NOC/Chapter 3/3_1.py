import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

angle = 0
aVelocity = 0
aAcceleration = 0.001

def setup():
    py5.create_screen(640, 360)

@py5.draw
def draw():
    global angle
    global aVelocity
    global aAcceleration

    py5.background(255)
    
    py5.fill(175)
    py5.stroke(0)
    py5.rect_mode(py5.CENTER)
    py5.translate(py5.width/2, py5.height/2)
    py5.rotate(angle)
    py5.line(-50, 0, 50, 0)
    py5.ellipse(50, 0, 8, 8)
    py5.ellipse(-50, 0, 8, 8)

    aVelocity += aAcceleration
    angle += aVelocity

setup()
draw()
