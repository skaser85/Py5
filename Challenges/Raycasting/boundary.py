class Boundary():
    def __init__(self, py5_inst, x1, y1, x2, y2):
        self.py5 = py5_inst
        self.a = self.py5.create_vector(x1, y1)
        self.b = self.py5.create_vector(x2, y2)

    def show(self):
        self.py5.stroke(255)
        self.py5.line(self.a.x, self.a.y, self.b.x, self.b.y)
        