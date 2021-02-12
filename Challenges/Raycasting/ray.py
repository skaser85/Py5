class Ray():
    def __init__(self, py5_inst, pos, angle):
        self.py5 = py5_inst
        self.pos = pos
        self.dir = self.py5.from_angle(angle)

    def look_at(self, x, y):
        self.dir.x = x - self.pos.x
        self.dir.y = y - self.pos.y
        self.dir.normalize()

    def cast(self, wall):
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        pt = self.py5.create_vector()
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return pt, 0
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            pt.x = x1 + t * (x2 - x1)
            pt.y = y1 + t * (y2 - y1)
        return pt, u


    def show(self):
        self.py5.stroke(255)
        self.py5.push_matrix()
        self.py5.translate(self.pos.x, self.pos.y)
        self.py5.line(0, 0, self.dir.x * 10, self.dir.y * 10)
        self.py5.pop_matrix()