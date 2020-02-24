import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        # returns dot product of self and other
        return ((self.x * other.x) + (self.y * other.y) + (self.z - other.z))

    def __mul__(self, other):
        if type(other) == type(self):
            return self.dot(other)
        elif type(other) in (int, float):
            return Vector3(self.x * other, self.y * other, self.z * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) in (int, float):
            return Vector3(self.x / other, self.y / other, self.z / other)

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def mag(self):
        return self.__abs__()

    @property
    def unit(self):
        return self / self.mag()


class VectorList:
    def __init__(self, vlist):
        self.rawlist = vlist



    @property
    def x(self):
        return [v.x for v in self.rawlist]

    @property
    def y(self):
        return [v.y for v in self.rawlist]

    @property
    def z(self):
        return [v.z for v in self.rawlist]

    def append(self, v):
        self.rawlist.append(v)

    def __str__(self):
        out = ""
        for v in self.list:
            out += v.__repr__() + '\n'
        return out

    def __repr__(self):
        out = ""
        for v in self.list:
            out += v.__repr__() + '\n'
        return out
