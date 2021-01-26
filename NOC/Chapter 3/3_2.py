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
        self.G = 0.4
        self.angle = 0
        self.aVelocity = 0
        self.aAcceleration = 0

    def is_inside(self, lq):
        return self.location.x > lq.x and\
               self.location.x < lq.x + lq.w and\
               self.location.y > lq.y and\
               self.location.y < lq.y + lq.h

    def drag(self, lq):
        speed = self.velocity.mag()
        dragMag = lq.c * speed * speed
        drag = self.velocity.copy()
        drag.mult(-1)
        drag.normalize()
        drag.mult(dragMag)
        self.apply_force(drag)

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

    def attract(self, m):
        force = Vector.static_sub(self.location, m.location)
        distance = force.mag()
        distance = Py5.constrain(distance, 5, 25)
        force.normalize()
        strength = (self.G * self.mass * m.mass) / (distance * distance)
        force.mult(strength)
        return force

    def update(self):
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity)

        self.aAcceleration = self.acceleration.x
        self.aVelocity += self.aAcceleration
        # self.aVelocity = Py5.constrain(self.aVelocity, -0.1, 0.1)
        self.angle += self.aVelocity

        self.acceleration.mult(0)

    def display(self):
        self.py5.stroke(0)
        self.py5.fill(100)
        self.py5.rect_mode(self.py5.CENTER)
        self.py5.push_matrix()
        self.py5.translate(self.location.x, self.location.y)
        self.py5.rotate(self.angle)
        self.py5.rect(0, 0, self.mass*16, self.mass*16)
        self.py5.pop_matrix()

movers = []

def setup():
    py5.create_screen(640, 360)
    for i in range(10):
        movers.append(Mover(py5, Py5.random_float_range(0.1, 2), Py5.random_int(py5.width), Py5.random_int(py5.height)))

@py5.draw
def draw():
    py5.background(255)

    for m in movers:
        for v in movers:
            if v != m:
                force = v.attract(m)
                m.apply_force(force)
        m.update()
        m.display()

setup()
draw()
