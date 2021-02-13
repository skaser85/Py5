class Drop():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.x = x
        self.y = y
        self.r = 6
        self.to_delete = False

    def evaporate(self):
        self.to_delete = True

    def hits(self, flower):
        d = self.py5.dist(self.x, self.y, flower.x, flower.y)
        return d < self.r + flower.r

    def move(self):
        self.y -= 30

    def show(self):
        self.py5.no_stroke()
        self.py5.fill(150, 0, 200)
        self.py5.ellipse(self.x + self.r, self.y, self.r * 2)