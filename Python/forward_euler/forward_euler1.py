import matplotlib
import sys
import math
from matplotlib import pyplot as plt
import pprint as pp
import time

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
        return math.sqrt(self.x**2 + self.y**2, self.z**2)
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
class VectorList:
    def __init__(self, vlist):
        self.rawlist = vlist
    
    @property
    def list(self):
        return self.rawlist
    @property
    def x(self):
        return [v.x for v in self.list]
    @property
    def y(self):
        return [v.y for v in self.list]
    @property
    def z(self):
        return [v.z for v in self.list]

    def append(self, v):
        self.list.append(v)
    
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

def main():

    dt = float(sys.argv[1])

    # Initial relative position
    r = Vector3(1, 0, 0)
    v = Vector3(0, 0.5, 0)

    r_list = VectorList([r])

    t = 0

    while t < 10:
        
        r_squared = (r.x*r.x + r.y*r.y + r.z*r.z)
        
        a = -1 * (r / (r_squared * math.sqrt(r_squared)))
        r = r + (v*dt)
        v = v + (a*dt)

        r_list.append(r)
        #v_list.append(v)
        t += dt
    
    #pp.pprint(r_list.x)
    plt.scatter(r_list.x,r_list.y, marker=".", s=1)
    plt.show()


if __name__ == "__main__":
    main()