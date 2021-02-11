import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

order = 7
N = int(py5.pow(2, order))
total = N * N
path = []
counter = 1

def setup():
    py5.create_screen(1024, 1024)
    # py5.create_screen(py5.FULLSCREEN)

    for i in range(total):
        path.append(hilbert(i))
        length = py5.width / N
        path[i].mult(length)
        path[i].add(length/2)

    py5.set_framerate(10)

def handle_resize():
    global path
    global counter
    path = []
    counter = 1
    setup()

py5.window_resized(handle_resize)

def hilbert(i):
    points = [
        py5.create_vector(0, 0),
        py5.create_vector(0, 1),
        py5.create_vector(1, 1),
        py5.create_vector(1, 0)
    ]
    index = i & 3
    v = points[index]
    for j in range(1, order):
        i = i >> 2
        index = i & 3
        length = py5.pow(2, j)
        if index == 0:
            temp = v.x
            v.x = v.y
            v.y = temp
        elif index == 1:
            v.y += length
        elif index == 2:
            v.x += length
            v.y += length
        elif index == 3:
            temp = length - 1 - v.x
            v.x = length - 1 - v.y
            v.y = temp
            v.x += length
    return v

@py5.draw
def draw():
    global counter
    py5.background(0)

    py5.no_fill()
    py5.stroke(255)
    py5.stroke_weight(2)
    for p in range(1, counter):
        p1 = path[p]
        p0 = path[p-1]
        r = p % 255
        g = (p * py5.random_int(255)) % 255
        py5.stroke(py5.random_int(255), py5.random_int(255), py5.random_int(255))
        py5.line(p1.x, p1.y, p0.x, p0.y)

    counter += 50

    if counter >= len(path):
        counter = 1

setup()
draw()
