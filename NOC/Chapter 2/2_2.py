import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from Vector import Vector
py5 = Py5()

class Mover():
    def __init__(self, py5inst, m, x, y):
        self.py5 = py5inst
        self.location = Py5.create_vector(x, y)
        self.velocity = Py5.create_vector(0, 0)
        self.acceleration = Py5.create_vector(0, 0)
        self.mass = m

    def apply_force(self, force):
        f = Vector.static_div(force, self.mass)
        self.acceleration.add(f)

    def check_edges(self):
        if self.location.x > self.py5.width:
            self.location.x = self.py5.width
            self.velocity.x *= -1
        elif self.location.x < 0:
            self.velocity.x *= -1
            self.location.x = 0

        if self.location.y > self.py5.height:
            self.location.y = self.py5.height
            self.velocity.y *= -1

    def update(self):
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity)
        self.acceleration.mult(0)

    def display(self):
        self.py5.stroke(0)
        self.py5.fill(175)
        self.py5.ellipse(self.location.x, self.location.y, self.mass*16, self.mass*16)

movers = []

def setup():
    py5.create_screen(640, 360)
    for i in range(100):
        mass = Py5.random_float_range(0.1, 5)
        movers.append(Mover(py5, mass, 0, 0))

@py5.draw
def draw():
    py5.background(255)

    wind = Vector(0.01, 0)
    gravity = Vector(0, 0.1)

    for m in movers:
        m.apply_force(wind)
        m.apply_force(gravity)
        m.update()
        m.check_edges()
        m.display()

setup()
draw()
