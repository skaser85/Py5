from Py5 import Py5
py5 = Py5()

a = 0.1

def setup():
    py5.create_screen(600, 600)
    py5.background(75)

@py5.draw
def draw():
    global a
    # py5.rotate(a)
    # a += 0.01

    # py5.rect_mode(py5.CENTER)
    # py5.stroke_weight(5)
    # py5.stroke(255,255,255, 255)
    # py5.fill(255, 0, 255, 128)
    # py5.rect(py5.width/2, py5.height/2, 100, 100)
    # py5.fill(0, 100, 150, 75)
    # py5.rect(py5.width/2+50,py5.height/2+50, 100, 100)

    py5.stroke_weight(5)
    py5.stroke(255, 255, 255, 255)
    py5.fill(255, 255, 0, 75)
    py5.circle(py5.width/2, py5.height/2, 100)
    py5.fill(255, 0, 128, 75)
    py5.circle(py5.width/2 - 50, py5.height/2 + 50, 100)



setup()
draw()
