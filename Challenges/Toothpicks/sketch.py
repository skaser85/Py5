import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Toothpick():
    def __init__(self, x, y, d):
        self.dir = d
        self.len = 63
        self.new_pick = True
        if self.dir == 1:
            self.ax = x - self.len / 2
            self.bx = x + self.len / 2
            self.ay = y
            self.by = y
        else:
            self.ax = x
            self.bx = x
            self.ay = y - self.len / 2
            self.by = y + self.len / 2

    def intersects(self, x, y):
        if self.ax == x and self.ay == y:
            return True
        elif self.bx == x and self.by == y:
            return True
        else:
            return False

    def create_a(self, others):
        available = True
        for o in others:
            if o is not self and o.intersects(self.ax, self.ay):
                available = False
        if available:
            return Toothpick(self.ax, self.ay, self.dir*-1)
        return None

    def create_b(self, others):
        available = True
        for o in others:
            if o is not self and o.intersects(self.bx, self.by):
                available = False
        if available:
            return Toothpick(self.bx, self.by, self.dir*-1)
        return None

    def show(self):
        py5.stroke(0)
        if self.new_pick:
            py5.stroke(0, 0, 255)
        py5.stroke_weight(2)
        py5.line(self.ax, self.ay, self.bx, self.by)

picks = []

def setup():
    py5.create_screen(600, 600)
    picks.append(Toothpick(0, 0, 1))

@py5.draw
def draw():
    py5.background(255)
    py5.translate(py5.width/2, py5.height/2)
    # py5.scale(.5)

    next_picks = []

    for p in picks:
        p.show()

    for p in picks:
        if p.new_pick:
            next_a = p.create_a(picks)
            next_b = p.create_b(picks)
            if next_a is not None:
                next_picks.append(next_a)
            if next_b is not None:
                next_picks.append(next_b)
            p.new_pick = False

    picks.extend(next_picks)

setup()
draw()
