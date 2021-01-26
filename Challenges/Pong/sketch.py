import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Ball():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.pos = Py5.create_vector(x, y)
        self.vel = Py5.create_vector(Py5.random_int_range(-6, 6), Py5.random_int_range(-6, 6))
        self.size = 32
        self.top = y - self.size/2
        self.bottom = self.top + self.size
        self.left = x - self.size/2
        self.right = self.left + self.size

    def reset(self):
        self.pos.x = self.py5.width/2
        self.pos.y = self.py5.height/2
        self.vel.x = Py5.random_int_range(-6, 6)
        self.vel.y = Py5.random_int_range(-6, 6)

    def update(self):
        did_reset = False
        side = ''
        self.pos.add(self.vel)
        if self.right > self.py5.width:
            self.reset()
            did_reset = True
            side = 'right'
        elif self.left < 0:
            self.reset()
            did_reset = True
            side = 'left'
        elif self.top < 0:
            self.pos.y = self.size/2
            self.vel.y *= -1
        elif self.bottom > self.py5.height:
            self.pos.y = self.py5.height - self.size
            self.vel.y *= -1
        self.top = self.pos.y - self.size/2
        self.bottom = self.top + self.size
        self.left = self.pos.x - self.size/2
        self.right = self.left + self.size
        return side, did_reset

    def check_paddles(self, rp, lp):
        if self.right > rp.left:
            if (self.bottom > rp.bottom and self.top < rp.bottom) or\
               (self.top < rp.top and self.bottom > rp.top) or\
               (self.top > rp.top and self.bottom < rp.bottom):
                self.pos.x = rp.left - self.size/2
                self.vel.x *= -1
        elif self.left < lp.right:
            if (self.bottom > lp.bottom and self.top < lp.bottom) or\
               (self.top < lp.top and self.bottom > lp.top) or\
               (self.top > lp.top and self.bottom < lp.bottom):
                self.pos.x = lp.right + self.size/2
                self.vel.x *= -1

    def draw(self):
        self.py5.fill(175)
        self.py5.circle(self.pos.x, self.pos.y, self.size)

class Paddle():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.pos = Py5.create_vector(x, y)
        self.w = 10
        self.h = 100
        self.top = y - self.h/2
        self.bottom = self.top + self.h
        self.left = x
        self.right = x + self.w

    def reset(self):
        self.pos.y = self.py5.height/2 - self.h/2

    def update(self, y_amt):
        self.pos.y += y_amt
        if self.pos.y < self.h/2:
            self.pos.y = self.h/2
        elif self.pos.y > self.py5.height - self.h/2:
            self.pos.y = self.py5.height - self.h/2
        # only need to update the top and bottom because the left
        # and right never move
        self.top = self.pos.y - self.h/2
        self.bottom = self.top + self.h

    def draw(self):
        self.py5.fill(255)
        self.py5.rect(self.pos.x, self.pos.y - (self.h/2), self.w, self.h)

# ==================== SKETCH STARTS HERE ===================================

MOVE_AMT = 10
p1_score = 0
p2_score = 0

def setup():
    py5.create_screen(960, 540)
    global thin
    global thick
    global marker
    global righteous
    global roboto_thin
    global roboto_regular
    global roboto_bold
    roboto_thin = py5.load_font(r'assets\Fonts\Roboto-Thin.ttf', 'roboto_thin')
    roboto_regular = py5.load_font(r'assets\Fonts\Roboto-Medium.ttf', 'roboto_regular')
    roboto_bold = py5.load_font(r'assets\Fonts\Roboto-Bold.ttf', 'roboto_bold')
    thin = py5.load_font(r'assets\Fonts\kenvector_future_thin.ttf', 'thin')
    thick = py5.load_font(r'assets\Fonts\kenvector_future.ttf', 'thick')
    marker = py5.load_font(r'assets\Fonts\PermanentMarker-Regular.ttf', 'marker')
    righteous = py5.load_font(r'assets\Fonts\Righteous-Regular.ttf', 'righteous')
    py5.text_size(28)
    global ball
    global r_paddle
    global l_paddle
    ball = Ball(py5, py5.width/2, py5.height/2)
    r_paddle = Paddle(py5, py5.width - 20, py5.height/2)
    l_paddle = Paddle(py5, 20, py5.height/2)

@py5.draw
def draw():
    global p1_score
    global p2_score

    py5.background(0)

    side, did_reset = ball.update()
    if did_reset:
        r_paddle.reset()
        l_paddle.reset()
        if side == 'right':
            p1_score += 1
        elif side == 'left':
            p2_score += 1

    pressed_keys = py5.get_pressed_keys()
    if pressed_keys:
        if pressed_keys[py5.UP_ARROW]:
            r_paddle.update(-MOVE_AMT)
        elif pressed_keys[py5.DOWN_ARROW]:
            r_paddle.update(MOVE_AMT)
        elif pressed_keys[py5.K_w]:
            l_paddle.update(-MOVE_AMT)
        elif pressed_keys[py5.K_s]:
            l_paddle.update(MOVE_AMT)

    ball.check_paddles(r_paddle, l_paddle)

    ball.draw()
    r_paddle.draw()
    l_paddle.draw()

    py5.text_font(roboto_regular)
    py5.fill(255, 0, 255)
    py5.text(f'P1 : {p1_score}', 10, 40)

    py5.text_font(roboto_bold)
    py5.fill(255, 255, 0)
    tw = py5.text_width(f'P2 : {p2_score}')
    py5.text(f'P2 : {p2_score}', py5.width - tw - 10, 40)


setup()
draw()
