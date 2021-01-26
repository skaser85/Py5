import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Mover():
    def __init__(self, py5):
        self.py5 = py5
        self.location = Py5.create_vector(py5.width/2, py5.height/2)
        self.velocity = Py5.create_vector(Py5.random(-2, 2), Py5.random(-2, 2))
        self.acceleration = Py5.create_vector(-0.001, 0.01)
        self.top_speed = 10

    def check_edges(self):
        if self.location.x > self.py5.width:
            self.location.x = 0
        elif self.location.x < 0:
            self.location.x = self.py5.width

        if self.location.y > self.py5.height:
            self.location.y = 0
        elif self.location.y < 0:
            self.location.y = self.py5.height

    def update(self):
        acceleration = Py5.random_2D()
        # Constant
        acceleration.mult(0.5)
        # Random
        # acceleration.mult(Py5.random(0, 2))

        self.velocity.add(acceleration)
        self.velocity.limit(self.top_speed)
        self.location.add(self.velocity)

    def display(self):
        self.py5.stroke(0)
        self.py5.fill(175)
        self.py5.ellipse(self.location.x, self.location.y, 32, 32)


mover = Mover(py5)

def setup():
    py5.create_screen(640, 360)

@py5.draw
def draw():
    py5.background(255)

    mover.update()
    mover.check_edges()
    mover.display()

setup()
draw()
