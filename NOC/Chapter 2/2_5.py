import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from Vector import Vector
py5 = Py5()

class Liquid():
    def __init__(self, x, y , w, h, c):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.c = c

    def display(self, py5_inst):
        py5_inst.fill(175)
        py5_inst.rect(self.x, self.y, self.w, self.h)

class Mover():
    def __init__(self, py5inst, m, x, y):
        self.py5 = py5inst
        self.location = Py5.create_vector(x, y)
        self.velocity = Py5.create_vector(0, 0)
        self.acceleration = Py5.create_vector(0, 0)
        self.mass = m

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

    def update(self):
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity)
        self.acceleration.mult(0)

    def display(self):
        self.py5.stroke(0)
        self.py5.fill(100)
        self.py5.ellipse(self.location.x, self.location.y, self.mass*16, self.mass*16)

movers = []
movers_count = 100

def setup():
    py5.create_screen(640, 360)
    global liquid
    liquid = Liquid(0, py5.height/2, py5.width, py5.height/2, 0.1)
    generate_movers(movers_count)

def generate_movers(n):
    for i in range(n):
        mass = Py5.random_float_range(0.1, 5)
        movers.append(Mover(py5, mass, Py5.random_int(py5.width), 0))

@py5.draw
def draw():
    global movers
    
    py5.background(255)

    liquid.display(py5)

    for m in movers:
        if m.is_inside(liquid):
            m.drag(liquid)
        gravity = Py5.create_vector(0, m.mass * 0.1)
        m.apply_force(gravity)
        m.update()
        m.check_edges()
        m.display()

    if py5.mouse_button_down():
        movers = []
        generate_movers(movers_count)

setup()
draw()
