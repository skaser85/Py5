import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Cell():
    def __init__(self, py5_inst, pos=None, r=None, c=None):
        self.py5 = py5_inst
        if pos is None:
            self.pos = self.py5.create_vector(self.py5.random_width(), self.py5.random_height())
        else:
            self.pos = pos
        if r is None:
            self.r = 60
        else:
            self.r = r
        if c is None:
            self.c = (self.py5.random_int_range(100, 255), 0, self.py5.random_int_range(100, 255), 75)
        else:
            self.c = c

    def clicked(self, m):
        d = self.py5.dist(self.pos, m)
        return d < self.r

    def mitosis(self):
        pos = self.py5.create_vector(self.pos.x + self.py5.random_int_range(-100, 100), self.pos.y)
        return Cell(self.py5, pos, self.r*0.8, self.c)

    def move(self):
        vel = self.py5.random_2D()
        vel.mult(1.5)
        self.pos.add(vel)
        if self.pos.x > self.py5.width:
            self.pos.x = self.py5.width
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y > self.py5.height:
            self.pos.y = self.py5.height
        if self.pos.y < 0:
            self.pos.y = 0

    def show(self):
        self.py5.fill(self.c)
        self.py5.circle(self.pos.x, self.pos.y, self.r)

cells = []

def setup():
    py5.create_screen(700, 700)
    cells.append(Cell(py5))
    cells.append(Cell(py5))

@py5.draw
def draw():
    py5.background(200)
    for cell in cells:
        cell.move()
        cell.show()

    m = py5.get_mouse_pos()
    if py5.mouse_clicked():
        for cell in reversed(cells):
            if cell.clicked(m):
                cells.append(cell.mitosis())
                cells.append(cell.mitosis())
                cells.remove(cell)


setup()
draw()
