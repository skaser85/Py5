import random
import math
import pygame
import functools
import numpy
from Vector import Vector

class Py5():
    """
    Py5 is a meager attempt at porting the p5.js drawing API
    into Python using the pygame library underneath to handle the
    actual interfacing with the OS and drawing things on the screen.
    """
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.width = 0
        self.height = 0
        self.screen = pygame.display.init()
        self.surface = None
        self.running = True
        self.background_set = False
        self.background_color = (0, 0, 0)
        self._stroke = True
        self.stroke_size = 0
        self.stroke_color = (0, 0, 0)
        self._fill = True
        self.fill_color = (0, 0, 0, 255)
        self.framerate = 60
        self.rotate_amt = 0
        self.old_rotate_amt = 0
        self.translate_x = 0
        self.translate_y = 0
        self.old_translate_x = 0
        self.old_translate_y = 0
        self.pressed_keys = []
        self.font = None
        self.fonts = []
        self.font_size = 28
        self.text_to_render = []
        self.vertices = []
        # CONSTANTS
        #  FONT
        self.NORMAL = 'normal'
        self.BOLD = 'bold'
        self.ITALIC = 'italic'
        self.BOLDITALIC = 'bolditalic'
        self.UNDERLINE = 'underline'
        self.TEXT_STYLE = self.NORMAL
        #   MATH
        self.PI = math.pi
        self.HALF_PI = math.pi / 2
        self.QUARTER_PI = math.pi / 4
        self.TAU = math.tau
        self.TWO_PI = math.tau
        self.DEGREES = 'degrees'
        self.RADIANS = 'radians'
        self.DEG_TO_RAD = math.pi / 180
        self.RAD_TO_DEG = 180 / math.pi
        self.ANGLE_MODE = self.DEGREES
        #   KEYS
        self.KEY_UP = False
        self.KEY_DOWN = True
        self.ALT = 18
        self.BACKSPACE = 8
        self.CONTROL = 17
        self.DELETE = 46
        self.DOWN_ARROW = pygame.K_DOWN
        self.UP_ARROW = pygame.K_UP
        self.LEFT_ARROW = pygame.K_LEFT
        self.RIGHT_ARROW = pygame.K_RIGHT
        self.ENTER = 13
        self.ESCAPE = 27
        self.OPTION = 18
        self.RETURN = 13
        self.SHIFT = 16
        self.TAB = 9
        self.K_w = pygame.K_w
        self.K_s = pygame.K_s
        #  MOUSE
        self.MOUSE_BUTTON_DOWN = False
        self.MOUSE_BUTTON_UP = False
        self._MOUSE_BUTTON_WAS_DOWN = False
        self._MOUSE_HAS_MOVED = False
        self._PREV_MOUSE = Vector(0, 0)
        self.MOUSE_X = 0
        self.MOUSE_Y = 0
        self.P_MOUSE_X = 0
        self.P_MOUSE_Y = 0
        self.MOVED_X = 0
        self.MOVED_Y = 0
        #  SHAPES
        self.RECT_MODE = 'corner'
        self.CORNER = 'corner'
        self.CENTER = 'center'

    def create_screen(self, w, h):
        """
        Creates a window to draw on.
        """
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode([w, h])
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)

    def background(self, r, g=None, b=None):
        """
        Sets the background of the screen.
        """
        if g and b is None:
            Py5.log_print('If function is called with more than 1 arg, it must be called with all 3', 'background', 'Py5')
            return
        self.background_set = True
        if g is not None and b is not None:
            self.background_color = (r, g, b)
        else:
            self.background_color = (r, r, r)

    def load_font(self, path, name):
        pygame.font.init()
        font = pygame.font.Font(path, self.font_size)
        if self.font is None:
            self.font = font
        self.fonts.append({'path': path, 'font': font, 'name': name})
        return font

    def text_font(self, font):
        self.font = font

    def text_size(self, n):
        self.font_size = n
        reset_font = False
        for font in self.fonts:
            if font['font'] == self.font:
                reset_font = True
            font['font'] = pygame.font.Font(font['path'], self.font_size)
            if reset_font:
                self.font = font['font']
                reset_font = False
        for text in self.text_to_render:
            text['rendered'] = self.font.render(text['raw'], True, self.fill_color)

    def text(self, t, x, y, x2=None, y2=None):
        self.text_to_render.append({
            'raw': t,
            'rendered': self.font.render(t, True, self.fill_color),
            'x': x,
            'y': y
        })

    def text_style(self, ts):
        if ts in [self.NORMAL, self.BOLD, self.ITALIC, self.BOLDITALIC, self.UNDERLINE]:
            self.TEXT_STYLE = ts
        if self.TEXT_STYLE == self.NORMAL:
            self.font.set_bold(False)
            self.font.set_italic(False)
            self.font.set_underline(False)
        elif self.TEXT_STYLE == self.BOLD:
            self.font.set_bold(True)
        elif self.TEXT_STYLE == self.ITALIC:
            self.font.set_italic(True)
        elif self.TEXT_STYLE == self.BOLDITALIC:
            self.font.set_bold(True)
            self.font.set_italic(True)
        elif self.TEXT_STYLE == self.UNDERLINE:
            self.font.set_underline(True)

    def text_width(self, t):
        return self.font.render(t, True, self.fill_color).get_width()

    def text_height(self, t):
        return self.font.render(t, True, self.fill_color).get_height()

    def text_ascent(self):
        return self.font.get_ascent()

    def text_descent(self):
        return self.font.get_descent()

    def load_pixels(self):
        pixels = []
        for i in range(self.surface.get_width()):
            for k in range(self.surface.get_height()):
                pixels.append(self.surface.get_at((i, k)))
        return pixels

    def update_pixels(self, pixels):
        for i in range(self.surface.get_width()):
            for k in range(self.surface.get_height()):
                index = i + k * self.width
                self.surface.set_at((i, k), pixels[index])

    def stroke(self, r, g=None, b=None, a=None):
        """
        Sets the stroke color.
        """
        if g and b is None:
            Py5.log_print('If function is called with more than 1 arg, it must be called with all 3', 'stroke', 'Py5')
            return
        if g is not None and b is not None and a is not None:
            self.stroke_color = (r, g, b, a)
        elif g is not None and b is not None:
            self.stroke_color = (r, g, b, 255)
        else:
            if isinstance(r, tuple):
                self.stroke_color = r
            else:
                self.stroke_color = (r, r, r, 255)
        if self.stroke_size < 0:
            self.stroke_size = 0
            self._stroke = False
        self._stroke = True

    def stroke_weight(self, sw):
        """
        Sets the stroke weight.
        """
        self.stroke_size = sw

    def no_stroke(self):
        """
        Turns off drawing a stroke around shapes.
        """
        self.stroke_size = 0
        self._stroke = False

    def no_fill(self):
        """
        Turns off filling in shapes.
        """
        self._fill = False
        self._stroke = True

    def fill(self, r, g=None, b=None, a=None):
        """
        Sets the fill color.
        """
        if g and b is None:
            Py5.log_print('If function is called with more than 1 arg, it must be called with all 3', 'fill', 'Py5')
            return
        if g is not None and b is not None and a is not None:
            self.fill_color = (r, g, b, a)
        elif g is not None and b is not None:
            self.fill_color = (r, g, b, 255)
        else:
            if isinstance(r, tuple):
                self.fill_color = r
            else:
                self.fill_color = (r, r, r, 255)
        self._fill = True

    def rect_mode(self, mode):
        # at some point, we'll support corners and radius modes
        if mode in ['corner', 'center']:
            self.RECT_MODE = mode

    def circle(self, x, y, size):
        """
        Draws a circle.
        """
        x += self.translate_x
        y += self.translate_y
        if self.RECT_MODE == 'center':
            x -= (size/2)
            y -= (size/2)
        if self._fill:
            self.draw_circle_fill((x, y), size)
        if self._stroke:
            self.draw_circle_border((x, y), size)

    def ellipse(self, x, y, size_x, size_y):
        """
        Draws an ellipse.
        """
        x += self.translate_x
        y += self.translate_y
        if self.RECT_MODE == 'center':
            x -= (size_x/2)
            y -= (size_y/2)
        if self._fill:
            self.draw_ellipse_fill(x, y, size_x, size_y)
        if self._stroke:
            self.draw_ellipse_border(x, y, size_x, size_y)

    def rect(self, x, y, w, h):
        """
        Draws a rectangle.
        """
        x += self.translate_x
        y += self.translate_y
        if self.RECT_MODE == 'center':
            x -= (w/2)
            y -= (h/2)
        rect = (x, y, w, h)
        if self._fill:
            self.draw_rect_fill(rect)
        if self._stroke:
            self.draw_rect_border(rect)

    def line(self, x1, y1, x2, y2):
        """
        Draws a line.
        """
        x1 += self.translate_x
        y1 += self.translate_y
        x2 += self.translate_x
        y2 += self.translate_y
        pygame.draw.line(self.surface, self.fill_color, (x1, y1), (x2, y2))

    def draw_rect_fill(self, rect):
        self.draw_rect_alpha(rect)

    def draw_rect_border(self, rect):
        self.draw_rect_alpha(rect, False)

    def draw_rect_alpha(self, rect, fill=True):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        shape_surf.set_colorkey(self.background_color)
        if fill:
            pygame.draw.rect(shape_surf, self.fill_color, shape_surf.get_rect())
        else:
            pygame.draw.rect(shape_surf, self.stroke_color, shape_surf.get_rect(), self.stroke_size)
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=(rect[0], rect[1]))
        self.surface.blit(shape_surf, shape_rect)

    def draw_circle_fill(self, center, radius):
        self.draw_circle_alpha(center, radius)

    def draw_circle_border(self, center, radius):
        self.draw_circle_alpha(center, radius, False)

    def draw_circle_alpha(self, center, radius, fill=True):
        target_rect = pygame.Rect((center), (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        if fill:
            pygame.draw.circle(shape_surf, self.fill_color, (radius, radius), radius)
        else:
            pygame.draw.circle(shape_surf, self.stroke_color, (radius, radius), radius, self.stroke_size)
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=center)
        self.surface.blit(shape_surf, shape_rect)

    def draw_ellipse_fill(self, x, y, rx, ry):
        self.draw_ellipse_alpha(x, y , rx, ry)

    def draw_ellipse_border(self, x, y, rx, ry):
        self.draw_ellipse_alpha(x, y, rx, ry, False)

    def draw_ellipse_alpha(self, x, y, rx, ry, fill=True):
        target_rect = pygame.Rect((x, y), (0, 0)).inflate((rx * 2, ry * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        if fill:
            pygame.draw.ellipse(shape_surf, self.fill_color, (x, y, rx, ry))
        else:
            pygame.draw.ellipse(shape_surf, self.stroke_color, (x, y, rx, ry), self.stroke_size)
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=(x,y))
        self.surface.blit(shape_surf, shape_rect)

    def draw_polygon_fill(self):
        self.draw_polygon_alpha()

    def draw_polygon_border(self):
        self.draw_polygon_alpha(False)

    def draw_polygon_alpha(self, fill=True):
        lx, ly = zip(*self.vertices)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        if fill:
            pygame.draw.polygon(shape_surf, self.fill_color, [(x - min_x, y - min_y) for x, y in self.vertices])
        else:
            pygame.draw.polygon(shape_surf, self.stroke_color, [(x - min_x, y - min_y) for x, y in self.vertices], self.stroke_size)
        self.surface.blit(shape_surf, target_rect)

    def begin_shape(self):
        self.vertices = []

    def end_shape(self):
        # probably need to pay attention to whether this needs to be CLOSED or not
        if len(self.vertices) > 0:
            if self._fill:
                self.draw_polygon_fill()
            if self._stroke:
                self.draw_polygon_border()

    def vertex(self, x, y):
        self.vertices.append((x, y))

    def push_matrix(self):
        self.old_translate_x = self.translate_x
        self.old_translate_y = self.translate_y
        self.old_rotate_amt = self.rotate_amt
        self.translate_x = 0
        self.translate_y = 0

    def pop_matrix(self):
        self.translate_x = self.old_translate_x
        self.translate_y = self.old_translate_y
        self.rotate_amt = self.old_rotate_amt
        self.old_translate_x = 0
        self.old_translate_y = 0
        self.old_rotate_amt = 0

    def translate(self, x, y):
        """
        Adds the passed-in values to the translation values.
        """
        self.translate_x += x
        self.translate_y += y

    def rotate(self, angle):
        self.rotate_amt += angle

    def angle_mode(self, mode):
        """
        Sets the angle mode for Py5.

        Valid modes: Py5.DEGREES or Py5.RADIANS
        """
        if mode in [self.DEGREES, self.RADIANS]:
            self.ANGLE_MODE = mode

    def set_framerate(self, val):
        """
        Sets the framerate.
        """
        self.framerate = val

    def mouse_button_down(self):
        """
        Returns a boolean that says whether the left mouse button is down.
        """
        return self.MOUSE_BUTTON_DOWN

    def mouse_button_up(self):
        """
        Returns a boolean that says whether the left mouse button is up.
        """
        return self.MOUSE_BUTTON_UP

    def mouse_pressed(self):
        """
        Returns a boolean that says whether the left mouse button is down and
        the left mouse button is NOT up (i.e., the left mouse button is being held down.)
        """
        return self.MOUSE_BUTTON_DOWN and not self.MOUSE_BUTTON_UP

    def get_pressed_keys(self):
        """
        Returns a list of keyboard keys that were pressed during the frame.
        """
        return self.pressed_keys

    @staticmethod
    def log_print(msg, name, file):
        # do some kind of log, too?
        print(f'{file} ::: {name} ::: {msg}')

    @staticmethod
    def get_mouse_pos():
        """
        Returns a Vector of the mouse's position.
        """
        m = pygame.mouse.get_pos()
        return Vector(m[0], m[1])

    @staticmethod
    def floor(val):
        """
        Returns the value floored.
        """
        return math.floor(val)

    @staticmethod
    def dist(x1, y1, x2, y2):
        """
        Returns the distance between the two points passed in.
        """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    @staticmethod
    def map(n, start1, stop1, start2, stop2, within_bounds):
        new_val = (n-start1)/(stop1-start1)*(stop2-start2)+start2
        if not within_bounds: # what even does this do?
            return new_val
        if start2 < stop2:
            return Py5.constrain(new_val, start2, stop2)
        else:
            return Py5.constrain(new_val, stop2, start2)

    @staticmethod
    def create_vector(x, y, z=0):
        """
        Returns a Vector based on the values passed in.
        """
        return Vector(x, y, z)

    @staticmethod
    def random_2D():
        """
        Returns a 2D vector with a random x and y.
        """
        return Vector.random_2D()

    @staticmethod
    def constrain(val, min_val, max_val):
        """
        Returns the value clamped between the min and max values passed in.
        """
        return min(max_val, max(min_val, val))

    @staticmethod
    def random():
        """
        Returns a random float between 0 and 1.
        """
        return random.random()

    @staticmethod
    def random_int(n):
        """
        Returns a random integer between 0 and the passed-in value.
        """
        return math.floor(random.random() * n)

    @staticmethod
    def random_float(n, prec=-1):
        """
        Returns a random float between 0 and the passed-in value.  If no 'prec'
        value is passed in, then the return value will not have any numbers after
        the decimal places.
        """
        return round(random.random() * n, prec)

    @staticmethod
    def random_int_range(mn=0, mx=0):
        """
        Returns a random integer between the min and max values passed in.
        """
        return random.randrange(mn, mx)

    @staticmethod
    def random_float_range(mn=0, mx=0):
        """
        Returns a random float between the min and max values passed in.
        """
        return random.uniform(mn, mx)

    def draw(self, draw_func):
        """
        Draws the objects from the instances draw function to the screen.
        """
        def wrapper():
            while self.running:

                self._MOUSE_BUTTON_WAS_DOWN = self.MOUSE_BUTTON_DOWN

                # Reset Py5 events
                self.KEY_UP = False
                self.KEY_DOWN = False
                self.MOUSE_BUTTON_UP = False
                self.MOUSE_BUTTON_DOWN = False

                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    # Did the user hit a key?
                    elif event.type == pygame.KEYDOWN:
                        self.KEY_DOWN = True
                    elif event.type == pygame.KEYUP:
                        self.KEY_UP = True
                        # Was it the Escape key? If so, stop the loop.
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                    elif event.type == pygame.MOUSEMOTION:
                        self._MOUSE_HAS_MOVED = True
                        self.P_MOUSE_X = self.MOUSE_X
                        self.P_MOUSE_Y = self.MOUSE_Y
                        mouse = pygame.mouse.get_pos()
                        self.MOUSE_X = mouse[0]
                        self.MOUSE_Y = mouse[1]
                        self.MOVED_X = self.MOUSE_X - self.P_MOUSE_X
                        self.MOVED_Y = self.MOUSE_Y - self.P_MOUSE_Y
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.MOUSE_BUTTON_DOWN = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.MOUSE_BUTTON_UP = True
                    
                if self._MOUSE_BUTTON_WAS_DOWN and not self.MOUSE_BUTTON_UP:
                    self.MOUSE_BUTTON_DOWN = True

                # Fill the background
                if self.background_set:
                    self.surface.fill(self.background_color)
                    self.background_set = False

                # Reset any state before the drawing happens again
                self.translate_x = 0
                self.translate_y = 0
                self.stroke_size = 1
                self.stroke_color = (0, 0, 0)
                self.fill_color = (0, 0, 0, 255)
                self._fill = False
                self._stroke = False
                self.vertices = []

                draw_func()

                # Draw text
                for t in self.text_to_render:
                    x = t['x'] + self.translate_x
                    y = t['y'] + self.translate_y
                    self.surface.blit(t['rendered'], (x, y))

                self.screen.blit(self.surface, (0, 0))


                # Flip the display
                pygame.display.flip()

                # Ensure program maintains a rate of consistent framerate
                self.clock.tick(self.framerate)

                self.pressed_keys = pygame.key.get_pressed()
                
                self.text_to_render = []

            # Done! Time to quit.
            pygame.quit()
        return wrapper
        