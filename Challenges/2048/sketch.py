import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
grandparentdir = os.path.dirname(parentdir)
sys.path.append(grandparentdir)
from Py5 import Py5
py5 = Py5()

class Tile():
    def __init__(self, py5_inst, x, y, w, h, num, tile_space, row, col):
        self.py5 = py5_inst
        self.pos = Py5.create_vector(x, y)
        self.num = num
        self.tile_space = tile_space
        self.row = row
        self.col = col
        self.w = w
        self.h = h
        self.color = (175, 175, 175)
        self.colors = {
            '2': (247, 241, 69),
            '4': (247, 214, 69),
            '8': (247, 197, 69),
            '16': (247, 143, 69),
            '32': (223, 247, 69),
            '64': (140, 247, 69),
            '128': (69, 247, 108),
            '256': (69, 247, 214),
            '512': (69, 208, 247),
            '1024': (69, 105, 247),
            '2048': (152, 69, 247),
            'o': (238, 69, 247)
        }

    def __repr__(self):
        return f'Tile -> tile: {self.tile_space}, col: {self.col}, row: {self.row}, num: {self.num}'

    def update(self, dir_vec):
        pass
        # if dir_vec.x:
        #     if dir_vec.x = 1:
                

    def draw(self):
        self.py5.fill(self.color)
        self.py5.rect(self.pos.x, self.pos.y, self.w, self.h)
        self.py5.fill(0)
        t = str(self.num)
        if self.colors.get(t):
            self.color = self.colors.get(t)
        else:
            self.color = self.colors.get('o')
        tw = self.py5.text_width(t)
        th = self.py5.text_height(t)
        tx = self.pos.x + (self.w/2) - (tw/2)
        ty = self.pos.y + (self.h/2) - (th/2)
        self.py5.text(t, tx, ty)
        self.py5.fill(255, 0, 255)


#============================== SKETCH STARTS HERE =====================================

gutter = 50

def place_tile(tile_space):
    tile_half_gutter = tile_gutter / 2
    tile_width = (width / 4) - tile_gutter
    tile_height = (height / 4) - tile_gutter
    row = Py5.floor(tile_space / 4)
    col = tile_space % 4
    x = tile_half_gutter + (col * qtr_w)
    y = tile_half_gutter + (row * qtr_h)
    num = 2
    r = Py5.random_float_range(0, 1)
    # if r > .5:
    #     num = 4
    # num = temp[i % len(temp)]
    tile = Tile(py5, x, y, tile_width, tile_height, num, tile_space, row, col)
    tile_spaces[tile_space]['tile'] = tile

def setup():
    py5.create_screen(400 + gutter, 400 + gutter)
    # py5.load_font(r'assets\Fonts\Roboto-Regular.ttf', 'roboto_regular')
    py5.load_font(r'assets\Fonts\PermanentMarker-Regular.ttf', 'marker')
    py5.text_size(28)

    global width
    global height
    global qtr_w
    global qtr_h
    global tiles
    global tile_gutter
    global smash

    width = py5.width - gutter
    height = py5.height - gutter
    qtr_w = width / 4
    qtr_h = height / 4
    smash = False

    global tile_spaces
    tile_spaces = [{'tile': None, 'updated': False} for t in range(16)]
    tile_gutter = 10
    place_tile(0)
    # place_tile(1)
    # place_tile(2)
    # place_tile(3)
    # temp = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    # for i in range(2):
    #     tile_placed = False
    #     while not tile_placed:
    #         tile_space = Py5.random_int(16)
    #         if tile_spaces[tile_space]['tile'] is None:
    #             tile_placed = True
    #             place_tile(tile_space)

@py5.draw
def draw():

    global tile_spaces
    global smash

    py5.background(255)
    py5.fill(255, 0, 0)

    py5.translate(gutter/2, gutter/2)
    py5.line(0, 0, width, 0)
    py5.line(width, 0, width, height)
    py5.line(0, height, width, height)
    py5.line(0, 0, 0, height)

    for i in range(3):
        q = qtr_w + (qtr_w * i)
        py5.line(q, 0, q, height)
    for i in range(3):
        q = qtr_h + (qtr_h * i)
        py5.line(0, q, width, q)


    direction = Py5.create_vector(0, 0)
    pressed_keys = py5.get_pressed_keys()
    if pressed_keys:
        if py5.KEY_UP:
            if pressed_keys[py5.UP_ARROW]:
                direction.y = -1
            elif pressed_keys[py5.DOWN_ARROW]:
                direction.y = 1
            elif pressed_keys[py5.RIGHT_ARROW]:
                direction.x = 1
            elif pressed_keys[py5.LEFT_ARROW]:
                direction.x = -1

    def check_smash(left, right):
        global smash
        if left and right:
            if left.num == right.num:
                right.num += left.num
                left = None
                smash = True
        elif left and not right:
            right = left
            right = None
        elif not left and right:
            pass
        return left, right

    def check_move(left, right):
        if left and not right:
            rx = left.pos.x + left.w + tile_gutter
            right = Tile(py5, rx, left.pos.y, left.w, left.h, left.num, left.tile_space + 1, left.row, left.col)
            left = None
        return left, right

    if direction.x or direction.y:
        if direction.x:
            rows = [tile_spaces[i:i+4] for i in range(0, 15, 4)]
            if direction.x == 1:
                for row in rows:
                    for i, r in enumerate(reversed(row)):
                        if i > 0:
                            pass
                    # smash = False
                    # row[2]['tile'], row[3]['tile'] = check_smash(row[2]['tile'], row[3]['tile'])
                    # row[0]['tile'], row[1]['tile'] = check_smash(row[0]['tile'], row[1]['tile'])
                    # if smash:
                    #     row[1]['tile'], row[2]['tile'] = check_move(row[1]['tile'], row[2]['tile'])
                    


    for t in tile_spaces:
        if t['tile'] is not None:
            t['tile'].draw()

setup()
draw()




                    # elif not smash and row[1]['tile'] and row[2]['tile']:
                    #     if row[1]['tile'].num == row[2]['tile'].num:
                    #         row[2]['tile'].num += row[1]['tile'].num
                    #         row[1]['tile'] = None
                    #         smash = True
                    # elif row[1]['tile'] and not row[2]['tile']:
                    #     if row[3]['tile']:
                    #         if not smash:
                    #             if row[3]['tile'].num == row[1]['tile'].num:
                    #                 row[3]['tile'].num += row[1]['tile'].num
                    #                 row[1]['tile'] = None
                    #                 smash = True
                    #         else:
                    #             row[2]['tile'] = row[1]['tile']
                    #             row[1]['tile'] = None
                    #     else:
                    #         row[3]['tile'] = row[1]['tile']
                    #         row[1]['tile'] = None
                        
                        
                            
                    # no check for smash - this is legal to smash now matter what
                    # if row[0]['tile'] and row[1]['tile']:
                    #     if row[0]['tile'].num == row[1]['tile']:
                    #         row[1]['tile'].num += row[0]['tile'].num
                    #         row[0]['tile'] = None
                    #         smash = True
                    # elif row[0]['tile'] and not row[1]['tile']:
                    #     row[1]['tile'] = row[0]['tile']
                    #     row[0]['tile'] = None
                    # elif row[0]['tile'] is None and row[1]['tile']:
                    #     pass

            # if direction.x == 1:
            #     rev_tile_spaces = list(reversed(tile_spaces))
            #     rows = [rev_tile_spaces[i:i+4] for i in range(0, 15, 4)]
            # for r in rows:
            #     for tile in r:
            #         if tile['tile'] is not None and not tile['updated']:
            #             tile['tile'].update(direction)
            #         else:
            #             tile['updated'] = True
        # if direction.y:
            # if direction.y == 1:
            #     # for tile in tile_spaces[::-1]:
            #     #     if tile['tile'] is not None and not tile['updated']:
            #     #         tile['tile'].update(direction)
            #     #     else:
            #     #         tile['updated'] = True
            #     rev_tile_spaces = list(reversed(tile_spaces))
            #     cols = [rev_tile_spaces[i:i+4] for i in range(4)]
            #     for c in cols:
            #         for tile in c:
            #             print(tile)
            #             if tile['tile'] is not None and not tile['updated']:
            #                 tile['tile'].update(direction)
            #             else:
            #                 tile['updated'] = True
            # else:
            #     cols = [tile_spaces[i::4] for i in range(4)]
            #     for c in cols:
            #         for tile in c:
            #             print(tile)
            #             if tile['tile'] is not None and not tile['updated']:
            #                 tile['tile'].update(direction)
            #             else:
            #                 tile['updated'] = True
        # tile_spaces = [{'tile': t['tile'], 'updated': False} for t in tile_spaces]




        # test_space = None
        # if dir_vec.x:
        #     test_col = self.col
        #     amt = (dir_vec.x * self.w)
        #     if dir_vec.x == 1:
        #         # moving right
        #         amt += 10
        #         test_col = self.col + 1
        #         # get tile to the right
        #         # don't do anything if we're on the right edge
        #         if self.tile_space not in [3, 7, 11, 15]:
        #             test_space = self.tile_space + 1
        #     else:
        #         # moving left
        #         amt -= 10
        #         test_col = self.col - 1
        #         # get tile to the left
        #         # don't do anything if we're on the left edge
        #         if self.tile_space not in [0, 4, 8, 12]:
        #             test_space = self.tile_space - 1
        #     if test_col >= 0 and test_col < 4:
        #         test_tile = tile_spaces[test_space]
        #         if test_tile['tile'] is None:
        #             self.pos.x += amt
        #             self.col = test_col
        #             tile_spaces[self.tile_space]['updated'] = True
        #             tile_spaces[self.tile_space]['tile'] = None
        #             tile_spaces[test_space]['tile'] = self
        #             tile_spaces[test_space]['updated'] = True
        #             self.tile_space = test_space
        # if dir_vec.y:
        #     test_row = self.row
        #     amt = (dir_vec.y * self.h)
        #     if dir_vec.y == 1:
        #         # moving down
        #         amt += 10
        #         test_row = self.row + 1
        #         # get the tile down one row
        #         # don't do anything if we're in the bottom row
        #         if self.tile_space not in [12, 13, 14, 15]:
        #             test_space = self.tile_space + 4
        #     else:
        #         # moving up
        #         amt -= 10
        #         test_row = self.row - 1
        #         # get the tile up one row
        #         # don't do anything if we're in the top row
        #         if self.tile_space not in [0, 1, 2, 3]:
        #             test_space = self.tile_space - 4
        #     if test_row >= 0 and test_row < 4:
        #         self.pos.y += amt
        #         self.row = test_row
        #         tile_spaces[self.tile_space]['updated'] = True
        #         tile_spaces[self.tile_space]['tile'] = None
        #         tile_spaces[test_space]['tile'] = self
        #         tile_spaces[test_space]['updated'] = True
        #         self.tile_space = test_space