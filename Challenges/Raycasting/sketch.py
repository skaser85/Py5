import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
from boundary import Boundary
from ray import Ray
from particle import Particle
from opensimplex import OpenSimplex
py5 = Py5()

open_simplex = OpenSimplex()
walls = []
ray = None
particle = None
x_off = 10000
y_off = 10000

def setup():
    global walls
    global ray
    global particle
    py5.create_screen(800, 800)
    for i in range(5):
        x1 = py5.random_width()
        x2 = py5.random_width()
        y1 = py5.random_height()
        y2 = py5.random_height()
        walls.append(Boundary(py5, x1, y1, x2, y2))
    walls.append(Boundary(py5, 0, 0, py5.width, 0))
    walls.append(Boundary(py5, py5.width, 0, py5.width, py5.height))
    walls.append(Boundary(py5, py5.width, py5.height, 0, py5.height))
    walls.append(Boundary(py5, 0, py5.height, 0, 0))
    ray = Ray(py5, 100, 200)
    particle = Particle(py5, py5.w2, py5.h2)

def handle_resize():
    global walls
    global ray
    global particle1
    walls = []
    ray = None
    particle = None
    setup()

py5.window_resized(handle_resize)

@py5.draw
def draw():
    global x_off
    global y_off
    py5.background(0)
    m = py5.get_mouse_pos()
    for wall in walls:
        wall.show()
    # x = open_simplex.noise2d(x_off * py5.width, particle.pos.y)
    # y = open_simplex.noise2d(particle.pos.x, y_off * py5.height)
    # particle.update_noise(x, y)
    # x_off += 1000000.01
    # y_off += 1000000.01
    particle.update(m.x, m.y)
    particle.show()
    particle.look(walls)
    

setup()
draw()
