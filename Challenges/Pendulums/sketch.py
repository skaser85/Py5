import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Pendulum():
    def __init__(self, py5_inst, x, y, r, bob_r):
        self.py5 = py5_inst
        self.origin = self.py5.create_vector(x, y)
        self.position = self.py5.create_vector(0, 0)
        self.r = r
        self.angle = self.py5.PI / 2
        self.aVelocity = 0.0
        self.aAcceleration = 0.0
        self.damping = 0.999
        self.ball_r = bob_r
        self.gravity = -.25

    def __repr__(self):
        return f'Pendulum -> position: {self.position}'

    def update(self):
        self.aAcceleration = (-1 * self.gravity / self.r) * self.py5.sin(self.angle)
        self.aVelocity += self.aAcceleration
        self.aVelocity *= self.damping
        self.angle += self.aVelocity

    def show(self):
        self.position.set_vec(self.r * self.py5.sin(self.angle), self.r * self.py5.cos(self.angle))
        self.position.add(self.origin)

        self.py5.stroke(252, 238, 33)
        self.py5.stroke_weight(1)
        self.py5.line(self.origin.x, self.origin.y, self.position.x, self.position.y)
        self.py5.fill(252, 238, 33, 200)
        self.py5.circle(self.position.x, self.position.y, self.ball_r)

penduls = []
spacing = 10

def setup():
    py5.create_screen(800, 800)
    total = py5.floor(py5.height / spacing)
    for i in range(total):
        penduls.append(Pendulum(py5, py5.width/2, py5.height, spacing + i * spacing, spacing))

def  handle_resize():
    global penduls
    penduls = []
    setup()

py5.window_resized(handle_resize)

@py5.draw
def draw():
    py5.background(112, 50, 126)
    for pendul in penduls:
        pendul.update()
        pendul.show()

setup()
draw()
