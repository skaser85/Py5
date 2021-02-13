class Ship():
    def __init__(self, py5_inst):
        self.py5 = py5_inst
        self.x = self.py5.w2
        self.size = 20

    def move(self, direction):
        self.x += direction * 20
    
    def show(self):
        self.py5.fill(255)
        self.py5.rect(self.x, self.py5.height - self.size, self.size, self.size * 3)
