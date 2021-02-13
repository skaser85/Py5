class Flower():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.x = x
        self.y = y
        self.r = 15
        self.x_speed = 10
        self.direction = 1
        self.y_speed = 10
        self.timer_length = 10
        self.timer = self.timer_length
        self.color = (self.py5.random_int(255), 0, self.py5.random_int(255))

    def update(self):
        self.x += self.x_speed * self.direction
        self.timer -= 1
        if self.timer == 0:
            self.y += self.y_speed
            self.direction *= -1
            self.timer = self.timer_length * 2

    def show(self):
        self.py5.fill(self.color)
        self.py5.ellipse(self.x, self.y, self.r * 2)
        self.py5.no_fill()
