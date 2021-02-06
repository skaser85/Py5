import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Turtle():
    def __init__(self, py5_inst, x, y, angle):
        self.py5 = py5_inst
        self.py5.translate(x, y)
        self.py5.rotate(angle)
        self.pen = True
        self.py5.stroke(255)
        self.py5.stroke_weight(2)

    def forward(self, amt):
        if self.pen:
            self.py5.line(0, 0, amt, 0)
        self.py5.translate(amt, 0)

    def backward(self, amt):
        self.forward(-amt)

    def right(self, angle):
        self.py5.rotate(angle)

commands = "fd 60 rt 120 fd 60 rt 120 fd 60 rt 120"
turtle = None

def setup():
    global turtle
    py5.create_screen(200, 200)
    py5.angle_mode(py5.DEGREES)
    tokens = commands.split()
    turtle = Turtle(py5, py5.width/2, py5.height/2, 0)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'fd':
            amt = tokens[i + 1]
            turtle.forward(int(amt))
            i += 2
        elif token == 'rt':
            angle = tokens[i + 1]
            turtle.right(int(angle))
            i += 2

@py5.draw
def draw():
    pass
    # py5.background(0)

setup()
draw()
