import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Drop():
    def __init__(self, py5_inst):
        self.py5 = py5_inst
        self.x = self.py5.random_width()
        self.y = self.py5.random_int_range(-1000, -50)
        self.z = self.py5.random_int(20)
        self.y_speed = self.py5.map(self.z, 0, 20, 4, 10)
        self.length = self.py5.map(self.z, 0, 20, 10, 20)
        self.thick = self.py5.map(self.z, 0, 20, 1, 3)


    def fall(self):
        self.y += self.y_speed
        grav = self.py5.map(self.z, 0, 20, 0, 0.2)
        self.y_speed += grav
        if self.y > self.py5.height:
            self.y = self.py5.random_int_range(-200, -100)
            self.y_speed = self.py5.map(self.z, 0, 20, 4, 10)
            return True
        return False

    def show(self):
        self.py5.stroke(purple)
        self.py5.stroke_weight(self.thick)
        self.py5.line(self.x , self.y, self.x, self.y + self.length)

class Splash():
    def __init__(self, py5_inst, x, weight):
        self.py5 = py5_inst
        self.x = x
        self.y = self.py5.height - weight / 2
        self.weight = weight / 2
        self.reverse = False

    def update(self):
        if self.y < self.py5.height - self.weight * 2:
            self.reverse = True
        if self.reverse:
            self.y += 1
        else:
            self.y -= 2

    def show(self):
        c = (purple[0], purple[1], purple[2], 75)
        self.py5.no_stroke()
        self.py5.fill(c)
        self.py5.circle(self.x + self.x/2, self.y, self.weight / 1.5)
        self.py5.circle(self.x - self.x/2, self.y, self.weight / 1.5)


purple = (138, 43, 226)
bg = (230, 230, 250)

drops = []
splashes = []

def setup():
    py5.create_screen(640, 360)
    for i in range(1000):
        drops.append(Drop(py5))

def handle_resize():
    global drops
    global splashes
    drops = []
    splashes = []
    setup()

py5.window_resized(handle_resize)

@py5.draw
def draw():
    py5.background(bg)
    for drop in drops:
        if drop.fall():
            splashes.append(Splash(py5, drop.x, drop.z))
        drop.show()
    if len(splashes) > 0:
        for splash in splashes:
            splash.show()
            splash.update()
            if splash.y > py5.height:
                splashes.remove(splash)

setup()
draw()
