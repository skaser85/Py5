import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Blob():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.pos = Py5.create_vector(x, y)
        self.vel = Py5.random_2D()
        self.vel.mult(Py5.random_float_range(2, 5))
        self.r = 15

    def update(self):
        self.pos.add(self.vel)
        if self.pos.x > self.py5.width or self.pos.x < 0:
            self.vel.x *= -1
        if self.pos.y > self.py5.height or self.pos.y < 0:
            self.vel.y *= -1

    def show(self):
        self.py5.stroke(0)
        self.py5.ellipse(self.pos.x, self.pos.y, self.r*2, self.r*2)

def setup():
    py5.create_screen(240, 180)
    global blobs
    blobs = []
    for i in range(5):
        blobs.append(Blob(py5, Py5.random_int(py5.width), Py5.random_int(py5.height)))
    
    py5.set_framerate(30)


@py5.draw
def draw():
    py5.background(51)

    pixels = py5.load_pixels()

    for x in range(py5.width):
        for y in range(py5.height):
            index = x + y * py5.width
            col_sum = 0
            for b in blobs:
                d = Py5.dist(x, y, b.pos.x, b.pos.y)
                if d == 0:
                    d = 1
                col = 500 * b.r / d
                col_sum += col
            col_sum = Py5.map(col_sum, 0, 700, 0, 255, True)
            pixels[index] = (col_sum, 100, 200, 255)

    py5.update_pixels(pixels)

    for b in blobs:
        b.update()


setup()
draw()
