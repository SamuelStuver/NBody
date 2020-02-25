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
        self.dot = Circle(Point(self.r.x,self.r.y), self.size)
        self.dot.setOutline("white")

    @property
    def size(self):
        return .01 * self.mass

    def draw(self, win):
        #win.plot(self.r.x, self.r.y, "white")
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

    def update(self, dt):
        self.r_0 = self.r
        self.r = self.r + (K2 * self.v * dt)
        self.v = self.v + (self.a * dt)

        self.dot.move(self.r.x - self.r_0.x, self.r.y - self.r_0.y)

    def randomize(self, max_mass=1, max_r=1, max_v=1):
        m = max_mass * random.random()

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
        self.rectangle.setOutline("white")

    def contains(self, body):
        min_x = self.x_center - self.width
        max_x = self.x_center + self.width
        min_y = self.y_center - self.height
        max_y = self.y_center + self.height
        return (min_x < body.r.x < max_x) and (min_y < body.r.y < max_y)

    def draw(self, win):
        self.rectangle.draw(win)



class QuadTree:
    # Each node has 4 quadrants that may or may not be empty
    def __init__(self, boundary, capacity=1):
        self.capacity = capacity
        self.boundary = boundary
        self.bodies = []
        self.divided = False

        # self.nw = QuadTree(boundary, capacity=self.capacity)
        # self.ne = QuadTree(boundary, capacity=self.capacity)
        # self.sw = QuadTree(boundary, capacity=self.capacity)
        # self.se = QuadTree(boundary, capacity=self.capacity)

        self.nw = self.ne = self.sw = self.se = None

    @property
    def totalMass(self):
        return sum([body.mass for body in self.bodies])

    @property
    def centerOfMass(self):
        x = sum([body.x * body.mass for body in self.bodies])
        y = sum([body.y * body.mass for body in self.bodies])
        z = sum([body.z * body.mass for body in self.bodies])
        return Vector3(x, y, z)/ self.totalMass

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


    def show(self, win):
        self.boundary.draw(win)
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


    max_r = 10
    max_v = 30
    max_mass = 1
    capacity = 1

    boundary = Quadrant(0, 0, max_r, max_r)
    qTree = QuadTree(boundary, capacity=capacity)

    N = int(sys.argv[1])
    for i in range(N):
        body = Body(index=i)
        body.randomize(max_mass=max_mass, max_r=max_r, max_v=max_v)
        qTree.insert(body)

    win = setupWindow(900, 900, 10, 10)

    # for i in range(N):
    #     print(i)
    #     mousePoint = win.checkMouse()
    #     if mousePoint:
    #         r = Vector3(mousePoint.getX() + random.uniform(-.1, .1), mousePoint.getY() + random.uniform(-.1, .1), 0)
    #         body = Body(r=r, index=i)
    #         qTree.insert(body)
    #         mousePoint = None
    #     time.sleep(.1)

    qTree.show(win)
    win.getMouse()