from opensimplex import OpenSimplex
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

rez = 5
cols = 0
rows = 0
field = []
noise = OpenSimplex(seed=py5.random_int(10000))
offset_incr = 0.1
z_off = 0

def setup():
    global cols
    global rows
    py5.create_screen(600, 400)
    cols = int(py5.width / rez) + 1
    rows = int(py5.height / rez) + 1
    for c in range(cols):
        field.append([])
        for r in range(rows):
            r = py5.floor(py5.random_int(2))
            field[c].append(r)

def handle_resize():
    global field
    global z_off
    field = []
    z_off = 0
    setup()

py5.window_resized(handle_resize)

def get_state(a, b, c, d):
    return a * 8 + b * 4 + c * 2  + d * 1

def line(p1, p2):
    py5.line(p1.x, p1.y, p2.x, p2.y)

@py5.draw
def draw():
    global z_off

    py5.background(127)

    x_off = 0
    y_off = 0

    for c in range(cols):
        x_off += offset_incr
        for r in range(rows):
            field[c][r] = noise.noise3d(x=x_off, y=y_off, z=z_off)
            y_off += offset_incr

    z_off += 0.03

    # for c in range(cols):
    #     for r in range(rows):
            # py5.stroke(py5.ceil(field[c][r]) * 255)
            # py5.stroke_weight(rez * .4)
            # py5.point(c * rez, r * rez)
            # py5.no_stroke()
            # py5.fill(py5.ceil(field[c][r]) * 255)
            # py5.rect(c*rez, r*rez, rez, rez)

    for i in range(cols - 1):
        for k in range(rows - 1):
            x = i * rez
            y = k * rez
            a = py5.create_vector(x + rez*.5, y)
            b = py5.create_vector(x + rez, y + rez*.5)
            c = py5.create_vector(x + rez*.5, y + rez)
            d = py5.create_vector(x, y + rez*.5)
            state = get_state(py5.ceil(field[i][k]), py5.ceil(field[i+1][k]), py5.ceil(field[i+1][k+1]), py5.ceil(field[i][k+1]))
            py5.stroke(255)
            py5.stroke_weight(1)
            if state == 0:
                pass
            elif state == 1:
                line(c, d)
            elif state == 2:
                line(b, c)
            elif state == 3:
                line(b, d)
            elif state == 4:
                line(a, b)
            elif state == 5:
                line(a, d)
                line(b, c)
            elif state == 6:
                line(a, c)
            elif state == 7:
                line(a, d)
            elif state ==8:
                line(a, d)
            elif state == 9:
                line(a, c)
            elif state == 10:
                line(a, b)
                line(c, d)
            elif state == 11:
                line(a, b)
            elif state == 12:
                line(b, d)
            elif state == 13:
                line(b, c)
            elif state == 14:
                line(c, d)


setup()
draw()
