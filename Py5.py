import ctypes
import random
import math
import pygame
from pygame import gfxdraw
import functools
import inspect
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
        self.screen_created = False
        self.screen = pygame.display.init()
        self.surface = None
        self.running = True
        self.background_set = False
        self.background_color = (0, 0, 0)
        self._stroke = True
        self.stroke_size = 0
        self.stroke_color = pygame.Color(0, 0, 0, 255)
        self._fill = True
        self.fill_color = (0, 0, 0, 255)
        self.framerate = 60
        self.rotate_amt = 0
        self.old_rotate_amt = 0
        self.translate_x = 0
        self.translate_y = 0
        self.old_translate_x = 0
        self.old_translate_y = 0
        self.scl = 1
        self.scl_int = 1
        self.pressed_keys = []
        self.font = None
        self.fonts = []
        self.font_size = 28
        self.text_to_render = []
        self.vertices = []
        self.should_loop = True
        self.do_redraw = False
        self.redraw_surface = None
        self.mouse_click_func = None
        self.first_frame_displayed = False
        self.frames = 0
        self.resize_func = None
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
        self.CLOSE = 'CLOSE'
        # WINDOW
        self.FULLSCREEN = 'fullscreen'
        self.WINDOW_WIDTH = 'window_width'
        self.WINDOW_HEIGHT = 'window_height'
        # COLOR
        self.COLOR_MODE = 'rgb'
        self.RGB = 'rgb'
        self.HSB = 'hsb'


    def create_screen(self, w=0, h=0, fullscreen=False):
        """
        Creates a window to draw on.
        """
        if not self.screen_created:
            self.screen_created = True
            py5_app = 'py5_app'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(py5_app)
            icon = pygame.image.load(r'icon\Py5_icon.png')
            pygame.display.set_caption('Py5 sketch')
            pygame.display.set_icon(icon)
            display_info = pygame.display.Info()
            if fullscreen or w == self.FULLSCREEN:
                self.width = display_info.current_w
                self.height = display_info.current_h
                self.screen = pygame.display.set_mode([0, 0], pygame.FULLSCREEN)
                self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                self.redraw_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            else:
                if w == self.WINDOW_WIDTH:
                    self.width = display_info.current_w
                elif isinstance(w, int):
                    self.width = w
                else:
                    print(f'Py5 :: create_screen :: invalid value passed for the "w" agrument.  Got {w} which is neither an integer nor the constant WINDOW_WIDTH.')
                if h == self.WINDOW_HEIGHT:
                    self.height = display_info.current_h
                elif isinstance(h, int):
                    self.height = h
                else:
                    print(f'Py5 :: create_screen :: invalid value passed for the "h" agrument.  Got {h} which is neither an integer nor the constant WINDOW_HEIGHT.')
                self.screen = pygame.display.set_mode([self.width, self.height], pygame.RESIZABLE)
                self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                self.redraw_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)


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

    def no_loop(self):
        self.should_loop = False

    def loop(self):
        self.should_loop = True

    def redraw(self):
        self.do_redraw = True

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

    def color_mode(self, mode, max_1, max_2, max_3, max_A=255):
        if mode in [self.RGB, self.HSB]:
            self.COLOR_MODE = mode
        else:
            print(f'Py5 :: color_mode :: unexpected color mode - got {mode} - valid modes [RGB, HSB]')
        if self._fill:
            self.fill(max_1, max_2, max_3, max_A)
        if self._stroke:
            self.stroke(max_1, max_2, max_3, max_A)

    def stroke(self, r, g=None, b=None, a=None):
        """
        Sets the stroke color.
        """
        if g and b is None:
            Py5.log_print('If function is called with more than 1 arg, it must be called with all 3', 'stroke', 'Py5')
            return
        if g is not None and b is not None and a is not None:
            if self.COLOR_MODE == 'rgb':
                self.stroke_color = pygame.Color(r, g, b, a)
            else:
                self.stroke_color = pygame.Color.hsla(r, g, b)
        elif g is not None and b is not None:
            if self.COLOR_MODE == 'rgb':
                self.stroke_color = pygame.Color(r, g, b, 255)
            else:
                self.stroke_color = pygame.Color.hsla(r, g, b)
        else:
            if isinstance(r, tuple):
                if self.COLOR_MODE == 'rgb':
                    self.stroke_color = pygame.Color(r[0], r[1], r[2])
                else:
                    self.stroke_color = pygame.Color.hsla(r[0], r[1], r[2])
            else:
                if self.COLOR_MODE == 'rgb':
                    self.stroke_color = pygame.Color(r, r, r, 255)
                else:
                    self.stroke_color = pygame.Color.hsla(r, r, r)
        if self.stroke_size < 0:
            self.stroke_size = 0
            self._stroke = False
        self._stroke = True

    def stroke_weight(self, sw):
        """
        Sets the stroke weight.
        """
        self.stroke_size = int(sw * self.scl)

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
            if self.COLOR_MODE == 'rgb':
                self.fill_color = pygame.Color(r, g, b, a)
            else:
                self.fill_color = pygame.Color.hsla(r, g, b)
        elif g is not None and b is not None:
            if self.COLOR_MODE == 'rgb':
                self.fill_color = pygame.Color(r, g, b, 255)
            else:
                self.fill_color = pygame.Color.hsla(r, g, b)
        else:
            if self.COLOR_MODE == 'rgb':
                if isinstance(r, tuple):
                    if len(r) == 3:
                        self.fill_color = pygame.Color(r[0], r[1], r[2])
                    elif len(r) == 4:
                        self.fill_color = pygame.Color(r[0], r[1], r[2], r[3])
                else:
                    self.fill_color = pygame.Color(r, r, r, 255)
            else:
                if isinstance(r, tuple):
                    self.fill_color = pygame.Color.hsla(r[0], r[1], r[2])
                else:
                    self.fill_color = pygame.Color.hsla(r, r, r)
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
        size *= self.scl
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
        size_x *= self.scl
        size_y *= self.scl
        if self.RECT_MODE == 'center':
            x -= (size_x/2)
            y -= (size_y/2)
        # @FIXME: for reasons that i am unable to work out, i can't get the alpha ellipses to draw anything
        # to the screen at all
        if self._fill:
            pygame.draw.ellipse(self.surface, self.fill_color, (x, y, size_x, size_y))
            # self.draw_ellipse_fill(x, y, size_x, size_y)
        if self._stroke:
            pygame.draw.ellipse(self.surface, self.stroke_color, (x, y, size_x, size_y), self.stroke_size)
            # self.draw_ellipse_border(x, y, size_x, size_y)

    def rect(self, x, y, w, h):
        """
        Draws a rectangle.
        """
        x += self.translate_x
        y += self.translate_y
        w *= self.scl
        h *= self.scl
        if self.RECT_MODE == 'center':
            x -= (w/2)
            y -= (h/2)
        rect = (x, y, w, h)
        if self._fill:
            self.draw_rect_fill(rect)
        if self._stroke:
            self.draw_rect_border(rect)

    def point(self, x, y):
        x += self.translate_x
        y += self.translate_y
        self.circle(x, y, self.stroke_size)

    def line(self, x1, y1, x2, y2):
        """
        Draws a line.
        """
        x1 += self.translate_x
        y1 += self.translate_y
        x2 += self.translate_x
        y2 += self.translate_y
        # line = pygame.draw.line(self.surface, self.stroke_color, (x1, y1), (x2, y2), self.stroke_size)
        # line.width *= self.scl
        # line.height *= self.scl
        #############################
        # length = self.dist(x1, y2, x2, y2)
        # length_scl = length * self.scl
        # p1 = Vector(x1, y1)
        # p2 = Vector(x2, y2)
        # if length_scl > length:
        #     p1.sub((length_scl/2))
        #     p2.add((length_scl/2))
        #     x1 -= (length_scl/2)
        #     y1 -= (length_scl/2)
        #     x2 += (length_scl/2)
        #     y2 += (length_scl/2)
        # else:
        #     p1.add((length_scl/2))
        #     p2.sub((length_scl/2))
        #     x1 += (length_scl/2)
        #     y1 += (length_scl/2)
        #     x2 -= (length_scl/2)
        #     y2 -= (length_scl/2)
        # pygame.draw.line(self.surface, (0, 255, 0), (p1.x, p1.y), (p2.x, p2.y), self.stroke_size)
        # temp = pygame.Surface(self.surface.get_size())
        # line = pygame.draw.line(temp, self.stroke_color, (x1, y1), (x2, y2), self.stroke_size)
        # line_rect = temp.get_rect()
        # temp = None
        # self.draw_line_alpha_test(line_rect, x1, y1, x2, y2)
        # print(self.stroke_color)
        pygame.draw.line(self.surface, self.stroke_color, (x1, y1), (x2, y2), self.stroke_size)
        # self.draw_line_alpha(line, x1, y1, x2, y2)

    def draw_line_alpha_test(self, line_rect, x1, y1, x2, y2):
        shape_surf = pygame.Surface((line_rect.w, line_rect.h), pygame.SRCALPHA)
        shape_surf.set_colorkey(self.background_color)
        pygame.draw.line(shape_surf, self.stroke_color, (x1, y1), (x2, y2), self.stroke_size)
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=line_rect.center)
        self.surface.blit(shape_surf, shape_rect)

    def draw_line_alpha(self, line, x1, y1, x2, y2):
        shape_surf = pygame.Surface((line.w, line.h), pygame.SRCALPHA)
        shape_surf.set_colorkey(self.background_color)
        pygame.draw.line(shape_surf, (0, 255, 0, 255), (line.x, line.y), (line.x, line.y))
        # @FIXME: this scaling doesn't actually work
        # shape_surf = pygame.transform.scale(shape_surf, (self.scl_int, self.scl_int))
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=line.center)
        self.surface.blit(shape_surf, shape_rect)

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

    def draw_polygon_fill(self, closed=False):
        self.draw_polygon_alpha(closed)

    def draw_polygon_border(self, closed=False):
        self.draw_polygon_alpha(closed, False)

    # def draw_polygon_alpha(self, fill=True):
    #     lx, ly = zip(*self.vertices)
    #     min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
    #     target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    #     shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    #     if fill:
    #         pygame.draw.polygon(shape_surf, self.fill_color, [(x - min_x, y - min_y) for x, y in self.vertices])
    #     else:
    #         # @Hack: need to do this in order to get all of the lines to show up; if it's anything less than 3, some
    #         # of the lines just won't show up
    #         if self.stroke_size < 3:
    #             self.stroke_size = 3
    #         pygame.draw.polygon(shape_surf, self.stroke_color, [(x - min_x, y - min_y) for x, y in self.vertices], self.stroke_size)
    #     shape_surf = pygame.transform.scale(shape_surf, (self.scl_int * target_rect.w, self.scl_int * target_rect.h))
    #     shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
    #     shape_rect = shape_surf.get_rect(center=target_rect.center)
    #     self.surface.blit(shape_surf, shape_rect)

    def draw_polygon_alpha(self, closed=False, fill=True):
        lx, ly = zip(*self.vertices)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        if fill:
            pygame.draw.polygon(shape_surf, self.stroke_color, [(x - min_x, y - min_y) for x, y in self.vertices])
        else:
            # @Hack: need to do this in order to get all of the lines to show up; if it's anything less than 3, some
            # of the lines just won't show up
            # if self.stroke_size < 3:
            #     self.stroke_size = 3
            pygame.draw.aalines(self.surface, self.stroke_color, closed, self.vertices, False)
            # pygame.draw.polygon(shape_surf, self.stroke_color, [(x - min_x, y - min_y) for x, y in self.vertices], self.stroke_size)
        shape_surf = pygame.transform.scale(shape_surf, (self.scl_int * target_rect.w, self.scl_int * target_rect.h))
        shape_surf = pygame.transform.rotate(shape_surf, self.rotate_amt)
        shape_rect = shape_surf.get_rect(center=target_rect.center)
        self.surface.blit(shape_surf, shape_rect)

    def begin_shape(self):
        self.vertices = []

    def end_shape(self, close=None):
        if len(self.vertices) > 2:
            if self._fill:
                if close == self.CLOSE:
                    self.draw_polygon_fill(closed=True)
                else:
                    self.draw_polygon_fill()
            if self._stroke:
                if close == self.CLOSE:
                    self.draw_polygon_border(closed=True)
                else:
                    self.draw_polygon_border()
        elif len(self.vertices) == 2:
            self.line(self.vertices[0][0], self.vertices[0][1], self.vertices[1][0], self.vertices[1][1])
        elif len(self.vertices) == 1:
            self.point(self.vertices[0][0], self.vertices[0][1])
        else:
            print(f'Py5 :: end_shape :: insufficient data to draw shape')

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

    def scale(self, scl):
        self.scl = scl
        self.scl_int = int(scl)

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

    def mouse_clicked(self):
        return self.MOUSE_BUTTON_UP

    def mouse_pressed(self):
        """
        Returns a boolean that says whether the left mouse button is down and
        the left mouse button is NOT up (i.e., the left mouse button is being held down.)
        """
        return self.MOUSE_BUTTON_DOWN and not self.MOUSE_BUTTON_UP

    def mouse_click(self, func):
        self.mouse_click_func = func

    def get_pressed_keys(self):
        """
        Returns a list of keyboard keys that were pressed during the frame.
        """
        return self.pressed_keys

    def window_resized(self, func):
        self.resize_func = func

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
    def ceil(val):
        return math.ceil(val)

    @staticmethod
    def dist(x1, y1, x2, y2):
        """
        Returns the distance between the two points passed in.
        """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    @staticmethod
    def map(n, start1, stop1, start2, stop2, within_bounds=True):
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

    @staticmethod
    def sin(angle):
        return math.sin(angle)

    @staticmethod
    def cos(angle):
        return math.cos(angle)

    @staticmethod
    def pow(num, exp):
        return math.pow(num, exp)

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
                    elif event.type == pygame.VIDEORESIZE:
                        self.width = event.w
                        self.height = event.h
                        self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                        self.surface = pygame.Surface((event.w, event.h), pygame.SRCALPHA)
                        self.redraw_surface = pygame.Surface((event.w, event.h), pygame.SRCALPHA)
                        if self.resize_func is None:
                            print(f'Py5 :: draw :: Window resize happened but no resize function existed.')
                        else:
                            self.resize_func()
                    
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

                if self.mouse_clicked() and self.mouse_click_func is not None:
                    self.mouse_click_func()

                if pygame.display.get_caption() == ('Py5 sketch', 'Py5 sketch'):
                    pygame.display.set_caption(f'{inspect.getfile(draw_func)}')

                # @FIXME: this doesn't work to show the first frame if no_loop
                if (self.should_loop or self.do_redraw) or (not self.first_frame_displayed):
                    draw_func()
                    # Draw text
                    for t in self.text_to_render:
                        x = t['x'] + self.translate_x
                        y = t['y'] + self.translate_y
                        self.surface.blit(t['rendered'], (x, y))
                    self.redraw_surface = pygame.Surface.copy(self.surface)
                    self.screen.blit(self.surface, (0, 0))
                    self.do_redraw = False
                    self.frames += 1
                    if self.frames > 1:
                        self.first_frame_displayed = True
                else:
                    self.screen.blit(self.redraw_surface, (0, 0))


                # Flip the display
                pygame.display.flip()

                # Ensure program maintains a rate of consistent framerate
                self.clock.tick(self.framerate)

                self.pressed_keys = pygame.key.get_pressed()

                self.text_to_render = []

            # Done! Time to quit.
            pygame.quit()
        return wrapper
        