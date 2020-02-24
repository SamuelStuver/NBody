from graphics import *
from vector import Vector3
from scipy.constants import G
import numpy as np
import random

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
        return .005 * self.mass

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

