import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Star():
    def __init__(self, py5_inst):
        self.py5 = py5_inst
        self.x = self.py5.random_width()
        self.y = self.py5.random_height()
        self.z = self.py5.random_width()
        if self.z == 0:
            self.z = 1
        self.pz = self.z

    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            self.x = self.py5.random_width()
            self.y = self.py5.random_height()
            self.z = self.py5.random_width()
            if self.z == 0:
                self.z = 1
            self.pz = self.z
            

    def show(self):
        self.py5.fill(255)
        self.py5.no_stroke()
        sx = (self.x / self.z)
        sx = self.py5.map(sx, 0, 1, 0, self.py5.width)
        sy = (self.y / self.z)
        sy = self.py5.map(sy, 0, 1, 0, self.py5.height)
        r = self.py5.map(self.z, 0, self.py5.width, 16, 0)
        # self.py5.ellipse(sx, sy, r)
        px = (self.x / self.pz)
        px = self.py5.map(px, 0, 1, 0, self.py5.width)
        py = (self.y / self.pz)
        py = self.py5.map(py, 0, 1, 0, self.py5.height)
        self.py5.stroke(255)
        self.py5.stroke_weight(1)
        self.py5.line(px, py, sx, sy)
        self.pz = self.z

stars = []

def setup():
    global stars
    py5.create_screen(1200, 800)
    for i in range(400):
        stars.append(Star(py5))

@py5.draw
def draw():
    py5.background(0)
    m = py5.get_mouse_pos()
    speed = py5.map(m.x, 0, py5.width, 1, 30)
    for star in stars:
        star.update(speed)
        star.show()

setup()
draw()
