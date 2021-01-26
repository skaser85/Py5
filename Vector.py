import math
import random

class Vector():
    """
    The Vector class defines 2D and 3D mathematical vectors as well providing
    various methods for working with them.
    """
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Vector -> x: {self.x}, y: {self.y}, z: {self.z}'

    @staticmethod
    def _is_finite(n):
        return not math.isinf(n)

    @staticmethod
    def _zero_check(n):
        return n != 0

    @staticmethod
    def _from_radians(angle, py5_inst):
        # if we want RADIANS, then just return the the angle
        if py5_inst.ANGLE_MODE == py5_inst.DEGREES:
            return angle *  py5_inst.RAD_TO_DEG
        return angle

    @staticmethod
    def _to_radians(angle, py5_inst):
        # if we want DEGREES, then just return the angle
        if py5_inst.ANGLE_MODE == py5_inst.RADIANS:
            return angle * py5_inst.DEG_TO_RAD
        return angle

    # This is called 'set_vec' instead of 'set' because 'set is a keyword
    # in Python, and I wanted to avoid as much confusion as possible.
    def set_vec(self, x, y=0, z=0):
        """
        Sets the x, y and z components of the instance.

        The x argument can be either a Vector, a List or a Number.
        """
        if isinstance(x, Vector):
            self.x = x.x
            self.y = x.y
            self.z = x.z
        elif isinstance(x, list):
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]
        else:
            self.x = x
            self.y = y
            self.z = z

    def copy(self):
        """
        Returns a new Vector with the x, y and z components matching
        the current instance.
        """
        return Vector(self.x, self.y, self.z)

    def add(self, x, y=None, z=None):
        """
        Sums the x, y and z components on the instance with whatever is passed in.

        The x argument can be either a Vector, a List or a Number.
        """
        if isinstance(x, Vector):
            self.x += x.x
            self.y += x.y
            self.z += x.z
        elif isinstance(x, list):
            self.x += x[0]
            self.y += x[1]
            self.z += x[2]
        else:
            if y is not None and z is not None:
                self.x += x
                self.y += y
                self.z += z
            else:
                self.x += x
                self.y += x
                self.z += x

    def sub(self, x, y=None, z=None):
        """
        Subtracts the x, y and z components on the instance with whatever is passed in.

        The x argument can be either a Vector, a List or a Number.
        """
        if isinstance(x, Vector):
            self.x -= x.x
            self.y -= x.y
            self.z -= x.z
        elif isinstance(x, list):
            self.x -= x[0]
            self.y -= x[1]
            self.z -= x[2]
        else:
            if y is not None and z is not None:
                self.x -= x
                self.y -= y
                self.z -= z
            else:
                self.x -= x
                self.y -= x
                self.z -= x

    def mult(self, x, y=None, z=None):
        """
        Multiplies the x, y and z components on the instance with whatever is passed in.

        The x argument can be either a Vector, a List or a Number.
        """
        if isinstance(x, Vector):
            self.x *= x.x
            self.y *= x.y
            self.z *= x.z
        elif isinstance(x, list):
            self.x *= x[0]
            self.y *= x[1]
            self.z *= x[2]
        else:
            if y is not None and z is not None:
                self.x *= x
                self.y *= y
                self.z *= z
            else:
                self.x *= x
                self.y *= x
                self.z *= x

    def div(self, x, y=None, z=None):
        """
        Divides the x, y and z components on the instance with whatever is passed in.

        The x argument can be either a Vector, a List or a Number.  If the x argument is either
        a Vector or a List, then if any of those components are 0 (zero), then the division will
        not be performed.  If the x argument is a Number, then if any of the x, y or z arguments
        passed in are 0 (zero), the division will not be performed.  If no division is performed,
        the instance x, y and z variables will not be changed.
        """
        if isinstance(x, Vector):
            v = self.array()
            all_finite = all(list(map(self._is_finite, v)))
            all_not_zero = all(list(map(self._zero_check, v)))
            if all_finite and all_not_zero:
                self.x /= x.x
                self.y /= x.y
                self.z /= x.z
        elif isinstance(x, list):
            all_finite = all(list(map(self._is_finite, x)))
            all_not_zero = all(list(map(self._zero_check, x)))
            if all_finite and all_not_zero:
                if len(x) == 2:
                    self.x /= x[0]
                    self.y /= x[1]
                elif len(x) == 3:
                    self.x /= x[0]
                    self.y /= x[1]
                    self.z /= x[2]
        else:
            if x == 0:
                return
            if y is not None:
                if y == 0:
                    return
                if z is not None:
                    if z == 0:
                        return
                    self.x /= x
                    self.y /= y
                    self.z /= z
            else:
                self.x /= x
                self.y /= x
                self.z /= x

    def rem(self, x, y=None, z=None):
        """
        Sets the x, y and z components to the remainder of the passed-in divisor.

        The x argument can be either a Vector, a List or a Number.
        """
        def calculate_remainder_2D(x_component, y_component):
            if x_component != 0:
                self.x = self.x % x_component
            if y_component != 0:
                self.y = self.y % y_component
        def calculate_remainder_3D(x_component, y_component, z_component):
            if x_component != 0:
                self.x = self.x % x_component
            if y_component != 0:
                self.y = self.y % y_component
            if z_component != 0:
                self.z = self.z % z_component

        if isinstance(x, Vector):
            if self._is_finite(x.x) and self._is_finite(x.y) and self._is_finite(x.z):
                x_component = x.x
                y_component = x.y
                z_component = x.z
                calculate_remainder_3D(x_component, y_component, z_component)
        elif isinstance(x, list):
            if all(list(map(self._is_finite, x))):
                if len(x) == 2:
                    calculate_remainder_2D(x[0], x[1])
                elif len(x) == 3:
                    calculate_remainder_3D(x[0], x[1], x[0])
        elif y is None and z is None:
            if(self._is_finite(x) and x != 0):
                self.x = self.x % x
                self.y = self.y % x
                self.z = self.z % z
        elif y is not None and z is None:
            if(self._is_finite(x) and self._is_finite(y)):
                calculate_remainder_2D(x, y)

    def mag_sq(self):
        """
        Returns the sum of the squares of each component:

        x*x + y*y + z*z
        """
        return self.x * self.x + self.y * self.y + self.z * self.z

    def mag(self):
        """
        Returns the magnitude (length) of the vector.
        """
        return math.sqrt(self.mag_sq())

    def cross(self, v):
        """
        Returns a new vector composed of the cross product between the passed-in
        vector and the instance.
        """
        x = self.y * v.z - self.z * v.y
        y = self.z * v.x - self.x * v.z
        z = self.x * v.y - self.y * v.x
        return Vector(x, y, z)

    def dot(self, x, y=0, z=0):
        """
        Returns the dot product of the passed-in vector and the instance.
        """
        if isinstance(x, Vector):
            return self.dot(x.x, x.y, x.z)
        else:
            return self.x * x + self.y * y + self.z *z

    def dist(self, v):
        """
        Returns the distance between the passed-in vector and the instance.
        """
        r = v.copy()
        r.sub(v)
        return r.mag()

    def normalize(self):
        """
        Sets the instance to a unit vector (normalize the instance to length 1)
        """
        m = self.mag()
        if m != 0:
            self.mult(1/m)

    def limit(self, n):
        """
        Limit the magnitude of the vector to the passed-in value.
        """
        m_sq = self.mag_sq()
        if(m_sq > n * n):
            self.normalize()
            self.mult(n)

    def set_mag(self, n):
        """
        Sets the magnitude of the instance to passed-in value.
        """
        self.normalize()
        self.mult(n)

    def heading(self, py5_inst):
        """
        Returns the angle of rotation for this instance (2D vectors only).  This
        will return a number either in DEGREES or RADIANS based on the current
        ANGLE_MODE of the passed-in Py5 instance.
        """
        h = math.atan2(self.x, self.y)
        return self._from_radians(h, py5_inst)

    def rotate(self, a, py5_inst):
        """
        Rotates the instance by the passed-in angle (2D vectors only).
        """
        new_heading = self.heading(py5_inst) + a
        mag = self.mag()
        self.x = math.cos(new_heading) * mag
        self.y = math.sin(new_heading) * mag

    def angle_between(self, v):
        """
        Returns the angle (in radians) between the passed in vector and the instance.
        """
        sign = lambda x : math.copysign(1, x)
        dotmagmag = self.dot(v) / (self.mag * v.mag())
        angle = math.acos(min(1, max(-1, dotmagmag)))
        s = sign(self.cross(v).z)
        if not s:
            s = 1
        angle = angle * s
        return angle

    def lerp(self, amt, x, y=0, z=0):
        """
        Performs a linear interpolation of the instance to the passed-in vector by the passed-in amount.
        """
        if isinstance(x, Vector):
            self.lerp(amt, x.x, x.y, x.z)
        else:
            self.x += (x - self.x) * amt
            self.y += (y - self.y) * amt
            self.z += (z - self.z) * amt

    def reflect(self, surface_normal):
        """
        Reflects the passed-in vector about a normal to a line in 2D, or about
        a normal to a plane in 3D.  This acts on the instance directly.
        """
        surface_normal.normalize()
        return self.sub(surface_normal.mult(2 * self.dot(surface_normal)))

    def array(self):
        """
        Returns a List of the instance's components.
        """
        return [self.x, self.y, self.z]

    def equals(self, x, y=0, z=0):
        """
        Checks if each of the components of the passed-in vector matches
        the components of the instance.
        """
        if isinstance(x, Vector):
            a = x.x
            b = x.y
            c = x.z
        elif isinstance(x, list):
            a = x[0]
            b = x[1]
            c = x[2]
        else:
            a = x
            b = y
            c = z
        return self.x == a and self.y == b and self.z == c

    @staticmethod
    def from_angle(angle, length=1):
        """
        Returns a new 2D vector from the passed-in angle.
        """
        return Vector(length * math.cos(angle), length * math.sin(angle))

    @staticmethod
    def from_angles(theta, phi, length=1):
        """
        Returns a new 3D vector from a pair of ISO spherical angles.
        """
        cosPhi = math.cos(phi)
        sinPhi = math.sin(phi)
        cosTheta = math.cos(theta)
        sinTheta = math.sin(theta)
        x = length * sinTheta * sinPhi
        y = -length * cosTheta
        z = length * sinTheta * cosPhi
        return Vector(x, y, z)

    @staticmethod
    def random_2D():
        """
        Returns a new 2D unit vector based on a random angle.
        """
        return Vector.from_angle(random.random() * math.tau)

    @staticmethod
    def random_3D():
        """
        Returns a new 3D unit vector.
        """
        angle = random.random() * math.tau
        vz = random.random() * 2 - 1
        vz_base = math.sqrt(1 - vz * vz)
        vx = vz_base * math.cos(angle)
        vy = vz_base * math.sin(angle)
        return Vector(vx, vy, vz)

    @staticmethod
    def static_add(v1, v2, target=None):
        """
        Returns a new vector of the sum of the two passed-in vectors.
        """
        if target is None:
            target = v1.copy()
        target.set_vec(v1)
        target.add(v2)
        return target

    @staticmethod
    def static_sub(v1, v2, target=None):
        """
        Returns a new vector of the difference of the two passed-in vectors.
        """
        if target is None:
            target = v1.copy()
        target.set_vec(v1)
        target.sub(v2)
        return target

    @staticmethod
    def static_mult(v, n, target=None):
        """
        Returns a new vector of the product of the two passed-in vectors.
        """
        if target is None:
            target = v.copy()
        target.set_vec(v)
        target.mult(n)
        return target

    @staticmethod
    def static_div(v, n, target=None):
        """
        Returns a new vecotr of the division of the two passed-in vectors.
        """
        if target is None:
            target = v.copy()
        target.set_vec(v)
        target.div(n)
        return target

    @staticmethod
    def static_rem(v1, v2, target=None):
        """
        Returns a new vector of the remainders of the two
        passed-in vectors after dividing the vectors.
        """
        if target is None:
            target = v1.copy()
        target = v1.copy()
        target.rem(v2)
        return target

    @staticmethod
    def static_dot(v1, v2):
        """
        Returns the dot product of the two passed-in vectors.
        """
        return v1.dot(v2)

    @staticmethod
    def static_cross(v1, v2):
        """
        Returns the corss product of the two passed-in vectors.
        """
        return v1.cross(v2)

    @staticmethod
    def static_dist(v1, v2):
        """
        Returns the distance of the two passed-in vectors.
        """
        return v1.dist(v2)

    @staticmethod
    def static_lerp(v1, v2, amt, target=None):
        """
        Returns a new vector after linearly interpolating between the
        two passed-in vectors.
        """
        if target is None:
            target = v1.copy()
        target.set_vec(v1)
        target.lerp(amt, v2)
        return target

    @staticmethod
    def static_mag(v):
        """
        Returns the magnitude of the passed in vector.
        """
        mag_sq = v.x * v.x + v.y * v.y + v.z * v.z
        return math.sqrt(mag_sq)
    