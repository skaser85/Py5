import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Cell():
    def __init__(self, py5_inst, i, j):
        self.py5 = py5_inst
        self.i = i
        self.j = j
        # top, right, bottom, left
        self.walls = [True, True, True, True]

    def show(self):
        x = self.i * w
        y = self.j * w
        self.py5.stroke(255)
        if self.walls[0]:
            self.py5.line(x, y, x+w, y)
        if self.walls[1]:
            self.py5.line(x+w,y,x+w,y+w)
        if self.walls[2]:
            self.py5.line(x+w,y+w,x,y+w)
        if self.walls[3]:
            self.py5.line(x,y+w,x,y)

cols = 0
rows = 0
w = 40
grid = []

def setup():
    global cols
    global rows
    py5.create_screen(401, 401)
    cols = py5.floor(py5.width/w)
    rows = py5.floor(py5.height/2)
    for j in range(rows):
        for i in range(cols):
            grid.append(Cell(py5, i, j))

@py5.draw
def draw():
    py5.background(51)

    for cell in grid:
        cell.show()

setup()
draw()
