import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from Vector import Vector

class Segment():
    def __init__(self):
        self.position = Py5.create_vector(0, 0)

class Snake():
    def __init__(self, py5, scl, x, y):
        self.py5 = py5
        self.x = x
        self.y = y
        self.scl = scl
        self.tail = [Segment()]
        self.dx = 1
        self.dy = 0

    def eat(self, pos):
        head = self.tail[0]
        d = Py5.dist(head.position.x, head.position.y, pos.x, pos.y)
        didEat = False
        if d < 1:
            self.tail.append(Segment())
            didEat = True
        return didEat
    
    def dir(self, x, y):
        self.dx = x
        self.dy = y

    def death(self):
        head = self.tail[0].position.copy()
        for i, seg in enumerate(self.tail):
            if i > 0:
                d = Py5.dist(head.x, head.y, seg.position.x, seg.position.y)
                if d < 1:
                    self.tail = [Segment()]

    def update(self):
        self.x += self.dx * self.scl
        self.y += self.dy * self.scl
        if self.x > self.py5.width:
            self.x = 0
        elif self.x < 0:
            self.x = self.py5.width
        if self.y > self.py5.height:
            self.y = 0
        elif self.y < 0:
            self.y = self.py5.height
        s1 = None
        s2 = None
        for i, seg in enumerate(self.tail):
            if i > 0:
                if s1:
                    s2 = seg.position.copy()
                    seg.position.set_vec(s1)
                    s1 = None
                elif s2:
                    s1 = seg.position.copy()
                    seg.position.set_vec(s2)
                    s2 = None
                else:
                    s1 = seg.position.copy()
                    seg.position.set_vec(self.tail[i-1].position)
        self.tail[0].position.x = self.x
        self.tail[0].position.y = self.y

    def show(self):
        self.py5.fill(255)
        for seg in self.tail:
            self.py5.rect(seg.position.x, seg.position.y, self.scl, self.scl)
