from ray import Ray

class Particle():
    def __init__(self, py5_inst, x, y):
        self.py5 = py5_inst
        self.pos = self.py5.create_vector(x, y)
        self.rays = []
        for i in range(0, 360, 1):
            self.rays.append(Ray(self.py5, self.pos, self.py5.radians(i)))
        print(self.pos)

    def look(self, walls):
        for ray in self.rays:
            closest = None
            record = self.py5.infinity()
            for wall in walls:
                pt, u = ray.cast(wall)
                if pt:
                    d = self.py5.dist(self.pos.x, self.pos.y, pt.x, pt.y)
                    if d < record:
                        record = d
                        closest = pt
            if closest:
                self.py5.stroke(255, 255, 255, 100)
                # self.py5.stroke(self.py5.random_int(100), self.py5.random_int(100), self.py5.random_int(100))
                self.py5.line(self.pos.x, self.pos.y, closest.x, closest.y)

    def update(self, x, y):
        self.pos.set_vec(x, y)

    def update_noise(self, x, y):
        self.pos.x += x
        self.pos.y += y

    def show(self):
        self.py5.fill(255)
        self.py5.ellipse(self.pos.x, self.pos.y, 4)
        for ray in self.rays:
            ray.show()
