import sys
import time
import math
from inspect import currentframe


class DebugTool:
    def __init__(self):
        try:
            self.fd = open(r"input.txt")
        except (ImportError, OSError):
            self.debug_mode = False
        else:
            import matplotlib.pyplot as plt
            self.plt = plt
            self.fg = None
            self.ax = None
            self.debug_mode = True
            self.timer = None

    def input(self):
        if self.debug_mode:
            data = self.fd.readline()
        else:
            data = input()
        print(data, file=sys.stderr, flush=True)
        return data

    def start_timer(self):
        self.timer = time.time()

    def elapsed_time(self):
        end_time = time.time()
        interval = end_time - self.timer
        self.stderr(interval * 1000, "m sec")

    @staticmethod
    def stderr(*args):
        cf = currentframe()
        print(*args, "@" + str(cf.f_back.f_lineno), file=sys.stderr, flush=True)

    def plot_vector_clock(self, vct, clr="b", txt=""):
        # todo: refactor in OO style
        self.plt.plot((0, vct[0]), (0, vct[1]), color=clr)
        self.plt.text(vct[0], vct[1], txt)


#######################################
# Classes for the contest
#######################################

class Vector(list):
    """
    This class is copied from kivy vector class.

    Find original source by using Search Everywhere
     and see module documentation for more information.
    """

    def __init__(self, *largs):
        if len(largs) == 1:
            super(Vector, self).__init__(largs[0])
        elif len(largs) == 2:
            super(Vector, self).__init__(largs)
        else:
            raise Exception('Invalid vector')

    def _get_x(self):
        return self[0]

    def _set_x(self, x):
        self[0] = x

    x = property(_get_x, _set_x)

    def _get_y(self):
        return self[1]

    def _set_y(self, y):
        self[1] = y

    y = property(_get_y, _set_y)

    def __getslice__(self, i, j):
        try:
            # use the list __getslice__ method and convert
            # result to vector
            return Vector(super(Vector, self).__getslice__(i, j))
        except Exception:
            raise TypeError('vector::FAILURE in __getslice__')

    def __add__(self, val):
        return Vector(list(map(lambda x, y: x + y, self, val)))

    def __iadd__(self, val):
        if type(val) in (int, float):
            self.x += val
            self.y += val
        else:
            self.x += val.x
            self.y += val.y
        return self

    def __neg__(self):
        return Vector([-x for x in self])

    def __sub__(self, val):
        return Vector(list(map(lambda x, y: x - y, self, val)))

    def __isub__(self, val):
        if type(val) in (int, float):
            self.x -= val
            self.y -= val
        else:
            self.x -= val.x
            self.y -= val.y
        return self

    def __mul__(self, val):
        try:
            return Vector(list(map(lambda x, y: x * y, self, val)))
        except Exception:
            return Vector([x * val for x in self])

    def __imul__(self, val):
        if type(val) in (int, float):
            self.x *= val
            self.y *= val
        else:
            self.x *= val.x
            self.y *= val.y
        return self

    def __rmul__(self, val):
        return (self * val)

    def __truediv__(self, val):
        try:
            return Vector(list(map(lambda x, y: x / y, self, val)))
        except Exception:
            return Vector([x / val for x in self])

    def __div__(self, val):
        try:
            return Vector(list(map(lambda x, y: x / y, self, val)))
        except Exception:
            return Vector([x / val for x in self])

    def __rtruediv__(self, val):
        try:
            return Vector(*val) / self
        except Exception:
            return Vector(val, val) / self

    def __rdiv__(self, val):
        try:
            return Vector(*val) / self
        except Exception:
            return Vector(val, val) / self

    def __idiv__(self, val):
        if type(val) in (int, float):
            self.x /= val
            self.y /= val
        else:
            self.x /= val.x
            self.y /= val.y
        return self

    def length(self):
        return math.sqrt(self[0] ** 2 + self[1] ** 2)

    def length2(self):
        return self[0] ** 2 + self[1] ** 2

    def distance(self, to):
        return math.sqrt((self[0] - to[0]) ** 2 + (self[1] - to[1]) ** 2)

    def distance2(self, to):
        return (self[0] - to[0]) ** 2 + (self[1] - to[1]) ** 2

    def normalize(self):
        if self[0] == 0. and self[1] == 0.:
            return Vector(0., 0.)
        return self / self.length()

    def dot(self, a):
        return self[0] * a[0] + self[1] * a[1]

    def angle(self, a):
        """Computes the angle between a and b, and returns the angle in
        degrees."""
        angle = -(180 / math.pi) * math.atan2(
            self[0] * a[1] - self[1] * a[0],
            self[0] * a[0] + self[1] * a[1])
        return angle

    def rotate(self, angle):
        """Rotate the vector with an angle in degrees."""
        angle = math.radians(angle)
        return Vector(
            (self[0] * math.cos(angle)) - (self[1] * math.sin(angle)),
            (self[1] * math.cos(angle)) + (self[0] * math.sin(angle)))

    @staticmethod
    def line_intersection(v1, v2, v3, v4):
        """
        Finds the intersection point between the lines (1)v1->v2 and (2)v3->v4
        and returns it as a vector object.

        >>> a = (98, 28)
        >>> b = (72, 33)
        >>> c = (10, -5)
        >>> d = (20, 88)
        >>> Vector.line_intersection(a, b, c, d)
        [15.25931928687196, 43.911669367909241]

        .. warning::

            This is a line intersection method, not a segment intersection.

        For math see: http://en.wikipedia.org/wiki/Line-line_intersection
        """
        # linear algebar sucks...seriously!!
        x1, x2, x3, x4 = float(v1[0]), float(v2[0]), float(v3[0]), float(v4[0])
        y1, y2, y3, y4 = float(v1[1]), float(v2[1]), float(v3[1]), float(v4[1])

        u = (x1 * y2 - y1 * x2)
        v = (x3 * y4 - y3 * x4)
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        px = (u * (x3 - x4) - (x1 - x2) * v) / denom
        py = (u * (y3 - y4) - (y1 - y2) * v) / denom

        return Vector(px, py)

    @staticmethod
    def segment_intersection(v1, v2, v3, v4):
        """
        Finds the intersection point between segments (1)v1->v2 and (2)v3->v4
        and returns it as a vector object.

        >>> a = (98, 28)
        >>> b = (72, 33)
        >>> c = (10, -5)
        >>> d = (20, 88)
        >>> Vector.segment_intersection(a, b, c, d)
        None

        >>> a = (0, 0)
        >>> b = (10, 10)
        >>> c = (0, 10)
        >>> d = (10, 0)
        >>> Vector.segment_intersection(a, b, c, d)
        [5, 5]
        """
        # Yaaay! I love linear algebra applied within the realms of geometry.
        x1, x2, x3, x4 = float(v1[0]), float(v2[0]), float(v3[0]), float(v4[0])
        y1, y2, y3, y4 = float(v1[1]), float(v2[1]), float(v3[1]), float(v4[1])
        # This is mostly the same as the line_intersection
        u = (x1 * y2 - y1 * x2)
        v = (x3 * y4 - y3 * x4)
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom == 0:
            return None

        px = (u * (x3 - x4) - (x1 - x2) * v) / denom
        py = (u * (y3 - y4) - (y1 - y2) * v) / denom
        # Here are the new bits
        c1 = (x1 <= px <= x2) or (x2 <= px <= x1)
        c2 = (y1 <= py <= y2) or (y2 <= py <= y1)
        c3 = (x3 <= px <= x4) or (x4 <= px <= x3)
        c4 = (y3 <= py <= y4) or (y4 <= py <= y3)

        if (c1 and c2) and (c3 and c4):
            return Vector(px, py)
        else:
            return None

    @staticmethod
    def in_bbox(point, a, b):
        """Return True if `point` is in the bounding box defined by `a`
        and `b`.

        >>> bmin = (0, 0)
        >>> bmax = (100, 100)
        >>> Vector.in_bbox((50, 50), bmin, bmax)
        True
        >>> Vector.in_bbox((647, -10), bmin, bmax)
        False

        """
        return ((a[0] >= point[0] >= b[0] or
                 b[0] >= point[0] >= a[0]) and
                (a[1] >= point[1] >= b[1] or
                 b[1] >= point[1] >= a[1]))


class Unit:
    def __init__(self, unit_id, player_id, radius, x, y):
        self.unit_id = int(unit_id)
        self.radius = int(radius)
        self.player_id = int(player_id)
        self.x = int(x)
        self.y = int(y)

        self.pos = self.x, self.y

    def distance2(self, unit_or_pos):
        """Return distance to the unit or the position."""
        # return self.cube().distance_to(unit_or_pos)
        if isinstance(unit_or_pos, Unit):
            pos = unit_or_pos.pos
        else:
            pos = unit_or_pos
        return Vector(self.pos).distance2(pos)


class Units(list):
    def __init__(self, unit_list=()):
        super().__init__(unit_list)

    def ally(self):
        class_name = type(self)
        return class_name([e for e in self if e.player_id == 0])  # type: class_name

    def enemy(self):
        class_name = type(self)
        return class_name([e for e in self if e.player_id > 0])  # type: class_name

    def closest_to(self, unit_or_pos):
        return min(self, key=lambda u: u.distance2(unit_or_pos))  # type: type(self)


class Reaper(Unit):
    def __init__(self, unit_id, player_id, mass, radius, x, y, vx, vy):
        super().__init__(unit_id, player_id, radius, x, y)
        self.mass = float(mass)
        self.vx = vx
        self.vy = vy


class Destroyer(Unit):
    def __init__(self, unit_id, player_id, mass, radius, x, y, vx, vy):
        super().__init__(unit_id, player_id, radius, x, y)
        self.mass = float(mass)
        self.vx = vx
        self.vy = vy


class Tanker(Unit):
    def __init__(self, unit_id, player_id, mass, radius, x, y, vx, vy, extra, extra2):
        super().__init__(unit_id, player_id, radius, x, y)
        self.mass = float(mass)
        self.vx = vx
        self.vy = vy
        self.water = extra
        self.cap = extra2


class Wreck(Unit):
    def __init__(self, unit_id, player_id, radius, x, y, extra):
        super(Wreck, self).__init__(unit_id, player_id, radius, x, y)
        self.water = extra


#######################################
# Debugger Instantiation
#######################################
DT = DebugTool()
DEBUG = False

#######################################
# Constant Values
#######################################
MY_PLAYER_ID = 0
REAPER = 0
DESTROYER = 1
TANKER = 3
WRECK = 4
MAX_THROTTLE = 300

#######################################
# Parameters to be adjusted
#######################################
# STRATEGY

#######################################
# Global Initialization
#######################################

#######################################
# Prefixed Command
#######################################

#######################################
# Game Loop
#######################################


while True:
    # Initialization for turn
    # They are used globally in the game
    reapers = Units()
    wrecks = Units()
    destroyers = Units()
    tankers = Units()

    # <<< Read Input >>>
    my_score = int(DT.input())
    enemy_score_1 = int(DT.input())
    enemy_score_2 = int(DT.input())
    my_rage = int(DT.input())
    enemy_rage_1 = int(DT.input())
    enemy_rage_2 = int(DT.input())
    unit_count = int(DT.input())

    for i in range(unit_count):
        unit_id, unit_type, player_id, mass, radius, x, y, vx, vy, extra, extra2 = DT.input().split()
        if int(unit_type) == REAPER:
            reapers.append(Reaper(unit_id, player_id, mass, radius, x, y, vx, vy))
        elif int(unit_type) == WRECK:
            wrecks.append(Wreck(unit_id, player_id, radius, x, y, extra))
        elif int(unit_type) == DESTROYER:
            destroyers.append(Destroyer(unit_id, player_id, mass, radius, x, y, vx, vy))
        elif int(unit_type) == TANKER:
            tankers.append(Tanker(unit_id, player_id, mass, radius, x, y, vx, vy, extra, extra2))

    # Main Logic
    # Choose Action
    my_reaper = reapers.ally()[0]
    my_destroyer = destroyers.ally()[0]

    if wrecks:
        reaper_target = wrecks.closest_to(my_reaper)
    else:
        reaper_target = my_destroyer

    if tankers:
        destroyer_target = tankers.closest_to(my_destroyer)
    else:
        destroyer_target = my_reaper

    # <<< Print Output >>>
    print("{0} {1} {2}".format(reaper_target.x, reaper_target.y, MAX_THROTTLE))
    print("{0} {1} {2}".format(destroyer_target.x, destroyer_target.y, MAX_THROTTLE))

    print("WAIT")
