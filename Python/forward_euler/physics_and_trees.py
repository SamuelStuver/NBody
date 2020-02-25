import sys
from graphics import *
from vector import Vector3
from scipy.constants import G
import numpy as np
import random
import time

#Reference quantities
m_nd=1.989e+30 #kg #mass of the sun
r_nd=1.496e+11 #m #distance between earth and sun
v_nd=30000 #m/s #relative velocity of earth around the sun
t_nd=3.154e+7 #s #orbital period of earth

#Net constants
K1=G*t_nd*m_nd/(r_nd**2*v_nd)
K2=v_nd*t_nd/r_nd

class Body:
    def __init__(self, mass=1, r=Vector3(0,0,0), v=Vector3(0,0,0), index=0):
        self.index = index
        self.mass = mass
        self.r = self.r_0 = r
        self.v = v
        self.a = Vector3(0,0,0)
        self.size = .01 * self.mass
        self.dot = Circle(Point(self.r.x,self.r.y), self.size)



    def draw(self, win, color="white"):
        #win.plot(self.r.x, self.r.y, "white")
        self.dot.setOutline(color)
        self.dot.draw(win)

    def erase(self, win):
        #win.plot(self.r.x, self.r.y, "black")
        self.dot.undraw()

    def add_acceleration(self, other):
        r = self.r - other.r
        r_squared = r * r

        # Calculate acceleration
        acc = -K1 * other.mass * r.unit / r_squared
        self.a = self.a + acc

    def add_acceleration_BH(self, node, theta=0.5):

        if self in node.bodies:
            return

        if node.isExternal():
            r = self.r - node.centerOfMass
            r_squared = r * r

            # Calculate acceleration
            acc = -K1 * node.totalMass * r.unit / r_squared
            self.a = self.a + acc
            return True

        else:
            s_d = node.boundary.width / abs(node.centerOfMass - self.r)
            if s_d < theta:
                r = self.r - node.centerOfMass
                r_squared = r * r

                # Calculate acceleration
                acc = -K1 * node.totalMass * r.unit / r_squared
                self.a = self.a + acc
                return True

            else:
                self.add_acceleration(node.nw)
                self.add_acceleration(node.ne)
                self.add_acceleration(node.sw)
                self.add_acceleration(node.se)

    def update(self, dt):
        self.r_0 = self.r
        self.r = self.r + (K2 * self.v * dt)
        self.v = self.v + (self.a * dt)

        print(f"a: {self.a}")
        print(f"v: {self.v}")
        print(f"r: {self.r}")
        self.dot.move(self.r.x - self.r_0.x, self.r.y - self.r_0.y)

    def randomize(self, max_mass=1, max_r=1, max_v=1):
        m = max_mass  * random.random()

        rx = random.uniform(-max_r, max_r)
        ry = random.uniform(-max_r, max_r)
        rz = 0

        vx = random.uniform(-max_v, max_v)
        vy = random.uniform(-max_v, max_v)
        vz = 0

        r = Vector3(rx, ry, rz)
        v = Vector3(vx, vy, vz)

        self.mass = m
        self.r = r
        self.v = v

        self.dot = Circle(Point(self.r.x, self.r.y), self.size)
        self.dot.setOutline("white")




class Quadrant:
    def __init__(self, x_center, y_center, width, height):
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height

        p1 = Point(self.x_center - self.width, self.y_center - self.height)
        p2 = Point(self.x_center + self.width, self.y_center + self.height)

        self.rectangle = Rectangle(p1,p2)
        #self.rectangle.setOutline("white")

    def contains(self, body):
        min_x = self.x_center - self.width
        max_x = self.x_center + self.width
        min_y = self.y_center - self.height
        max_y = self.y_center + self.height
        return (min_x < body.r.x < max_x) and (min_y < body.r.y < max_y)

    def draw(self, win, color="white"):
        self.rectangle.setOutline(color)
        self.rectangle.draw(win)

    def intersects(self, range):
        return not (range.x_center - range.width > self.x_center + self.width) or \
                   (range.x_center + range.width < self.x_center - self.width) or \
                   (range.y_center - range.height > self.y_center + self.height) or \
                   (range.y_center + range.height < self.y_center - self.height)


class QuadTree:
    # Each node has 4 quadrants that may or may not be empty
    def __init__(self, boundary, capacity=1):
        self.capacity = capacity
        self.boundary = boundary
        self.bodies = []
        self.divided = False

        self.totalMass = 0
        self.centerOfMass = Vector3(0,0,0)

        self.nw = self.ne = self.sw = self.se = None

    # @property
    # def totalMass(self):
    #     return sum([body.mass for body in self.query(self.boundary)])
    #
    # @property
    # def centerOfMass(self):
    #     x = sum([body.x * body.mass for body in self.query(self.boundary)])
    #     y = sum([body.y * body.mass for body in self.query(self.boundary)])
    #     z = sum([body.z * body.mass for body in self.query(self.boundary)])
    #     return Vector3(x, y, z)/ self.totalMass

    def isExternal(self):
        return (self.nw == self.ne == self.sw == self.se) is None

    def subdivide(self):
        x_center = self.boundary.x_center
        y_center = self.boundary.y_center
        w = self.boundary.width
        h = self.boundary.height

        nw = Quadrant(x_center - w / 2, y_center + h / 2, w / 2, h / 2)
        ne = Quadrant(x_center + w / 2, y_center + h / 2, w / 2, h / 2)
        sw = Quadrant(x_center - w / 2, y_center - h / 2, w / 2, h / 2)
        se = Quadrant(x_center + w / 2, y_center - h / 2, w / 2, h / 2)
        self.nw = QuadTree(nw, capacity=self.capacity)
        self.ne = QuadTree(ne, capacity=self.capacity)
        self.sw = QuadTree(sw, capacity=self.capacity)
        self.se = QuadTree(se, capacity=self.capacity)

        self.divided = True

    def insert(self, body):
        # If body does not go within the bounds of this section, return
        if not (self.boundary.contains(body)):
            return False
        # If number of bodies < capacity, append body to list of bodies
        # Else if capacity is full, subdivide
        if len(self.bodies) < self.capacity:
            # print(f"{body.index} - ({self.boundary.x_center},{self.boundary.y_center}) ")
            self.bodies.append(body)
            self.totalMass += body.mass
            self.centerOfMass = self.centerOfMass + Vector3((body.r.x * body.mass)/self.totalMass,
                                                            (body.r.y * body.mass)/self.totalMass,
                                                            (body.r.z * body.mass)/self.totalMass)
            return True

        elif not self.divided:
            self.subdivide()
        else:
            pass
        # Try to add body to each quadrant
        if self.nw and self.nw.insert(body):
            return True
        elif self.ne and self.ne.insert(body):
            return True
        elif self.sw and self.sw.insert(body):
            return True
        elif self.se and self.se.insert(body):
            return True

    def query(self, qRange):
        found = []
        if not self.boundary.intersects(qRange):
            # Empty
            return found
        else:
            for body in self.bodies:
                if qRange.contains(body):
                    found.append(body)

        if self.divided:
            found.extend(self.nw.query(qRange))
            found.extend(self.ne.query(qRange))
            found.extend(self.sw.query(qRange))
            found.extend(self.se.query(qRange))

        return found

    def populate_random(self, N=10, max_mass=1, max_r=10, max_v=30):
        for i in range(N):
            body = Body(index=i)
            body.randomize(max_mass=max_mass, max_r=max_r, max_v=max_v)
            self.insert(body)

    def populate_from_list(self, bodies):
        for body in bodies:
            self.insert(body)

    def show(self, win):
        # print(f"({self.boundary.x_center},{self.boundary.y_center}) - N Bodies: {self.nBodies}")
        #self.boundary.draw(win)
        for b in self.bodies:
            b.draw(win)
        if self.divided:
            self.nw.show(win)
            self.ne.show(win)
            self.sw.show(win)
            self.se.show(win)


    def __str__(self):
        out = ""
        for att in vars(self):
            out += f"{att}: {self.__dict__[att]}\n"

        return out

    def __repr(self):
        return self.__str__()


def setupWindow(x_pix_size, y_pix_size, xsize, ysize):
    win = GraphWin("NBody", x_pix_size, y_pix_size)
    win.setBackground("black")
    win.setCoords(-xsize, -ysize, xsize, ysize)
    return win



if __name__ == "__main__":

    N = int(sys.argv[1])

    max_r = 10
    max_v = 30
    max_mass = 1
    capacity = 1

    boundary = Quadrant(0, 0, max_r, max_r)
    qTree = QuadTree(boundary, capacity=capacity)
    qTree.populate_random(N=N, max_mass=1, max_r=10, max_v=30)



    win = setupWindow(900, 900, 10, 10)
    qTree.show(win)
    win.getMouse()

    qRange = Quadrant(1, 1, .27, .33)
    qRange.draw(win, color="red")
    win.getMouse()