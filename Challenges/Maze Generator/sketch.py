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
        self.visited = False

    def __repr__(self):
        return f'Cell -> i: {self.i} :: j: {self.j}'

    @staticmethod
    def index(i, j):
        if i < 0 or j < 0 or i > cols-1 or j > rows-1:
            return None
        return i + j * cols

    def check_neighbors(self):
        neighbors = []
        for n in range(4):
            if n == 0:
                idx = self.index(self.i, self.j-1)
            elif n == 1:
                idx = self.index(self.i+1, self.j)
            elif n == 2:
                idx = self.index(self.i, self.j+1)
            elif n == 3:
                idx = self.index(self.i-1,self.j)
            if idx:
                if not grid[idx].visited:
                    neighbors.append(grid[idx])
        if len(neighbors) > 0:
            r = self.py5.floor(py5.random_int(len(neighbors)))
            return neighbors[r]

    def show(self):
        x = self.i * w
        y = self.j * w
        self.py5.stroke(255, 255, 255)
        self.py5.stroke_weight(1)
        if self.walls[0]:
            self.py5.line(x, y, x+w, y)
        if self.walls[1]:
            self.py5.line(x+w,y,x+w,y+w)
        if self.walls[2]:
            self.py5.line(x+w,y+w,x,y+w)
        if self.walls[3]:
            self.py5.line(x,y+w,x,y)
        if self.visited:
            x += w/2
            y += w/2
            self.py5.no_stroke()
            self.py5.fill(255, 0, 255, 100)
            self.py5.rect(x, y, w, w)

    def highlight(self):
        x = self.i * w
        y = self.j * w
        x += w/2
        y += w/2
        self.py5.no_stroke()
        self.py5.fill(0, 255, 0, 255)
        self.py5.rect(x, y, w, w)


cols = 0
rows = 0
w = 20
grid = []
current = None
stack = []

def setup():
    global cols
    global rows
    global current
    py5.create_screen(801, 801)
    cols = py5.floor(py5.width/w)
    rows = py5.floor(py5.height/w)
    for j in range(rows):
        for i in range(cols):
            grid.append(Cell(py5, i, j))
    current = grid[0]

def handle_resize():
    global grid
    grid = []
    setup()

py5.window_resized(handle_resize)

@py5.draw
def draw():
    global current
    py5.background(51)

    for cell in grid:
        cell.show()

    current.visited = True
    current.highlight()
    neighbor = current.check_neighbors()
    if neighbor:
        stack.append(current)
        remove_walls(current, neighbor)
        neighbor.visited = True
        current = neighbor
    elif len(stack) > 0:
        current = stack.pop()

    if len(stack) > 0:
        for cell in stack:
            x = cell.i * w
            y = cell.j * w
            x += w/2
            y += w/2
            py5.no_stroke()
            py5.fill(0, 255, 255, 75)
            py5.rect(x, y, w, w)


def remove_walls(a, b):
    x = a.i - b.i
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    y = a.j - b.j
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False

setup()
draw()
