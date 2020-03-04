import sys
from graphics import *
from vector import Vector3
from scipy.constants import G
import random
import time
from display import WINDOW

#Reference quantities
m_nd=1.989e+30 #kg #mass of the sun
r_nd=1.496e+11 #m #distance between earth and sun
v_nd=30000 #m/s #relative velocity of earth around the sun
t_nd=3.154e+7 #s #orbital period of earth

#Net constants
K1=G*t_nd*m_nd/(r_nd**2*v_nd)
K2=v_nd*t_nd/r_nd

def calc_acceleration(target_r, other_r, other_mass):
    r = other_r - target_r
    r_squared = r * r

    # Calculate acceleration
    acceleration = (-K1 * other_mass * r.unit / r_squared)
    assert acceleration
    return acceleration


def drawLine(p1, p2, color):
    line = Line(p1, p2)
    line.setOutline(color)
    line.undraw()
    line.draw(WINDOW)
    return line

def eraseLine(line):
    line.undraw()


class Body:
    def __init__(self, mass=1, r=Vector3(0,0,0), v=Vector3(0,0,0), index=0):
        self.index = index
        self.mass = mass
        self.r = self.r_0 = r
        self.v = v
        self.a = Vector3(0,0,0)
        self.size = .01 * self.mass
        self.dot = Circle(Point(self.r.x,self.r.y), self.size)

    def __eq__(self, other):
        if isinstance(other, Body):
            return self.index == other.index
        elif isinstance(other, QuadTree):
            return len(other.query(other.boundary)) and abs(self.r - other.centerOfMass) < 0.001

    def draw(self, color="white"):
        self.dot.setOutline(color)
        self.dot.undraw()
        self.dot.draw(WINDOW)

    def erase(self):
        self.dot.undraw()

    def check_theta(self, node, theta):
        if not node:
            return "STUFF1"

        if (not node.divided) and (len(node.bodies) > 0) and self not in node.query(node.boundary):
            line = drawLine(Point(self.r.x, self.r.y), Point(node.bodies[0].r.x, node.bodies[0].r.y), "red")
            eraseLine(line)
            if abs(node.bodies[0].r - self.r) > 0:
                acceleration = calc_acceleration(self.r, node.bodies[0].r, node.bodies[0].mass)
                print(acceleration)
                return "STUFF2"
                return acceleration # calculate acc from single point


        if node.divided:
            node_center_of_mass = Vector3(0,0,0)
            for b in node.query(node.boundary):
                node_center_of_mass.x += (b.mass * b.r.x)/node.totalMass
                node_center_of_mass.y += (b.mass * b.r.y)/node.totalMass
                node_center_of_mass.z += (b.mass * b.r.z)/node.totalMass
            self.erase()
            self.draw(color="red")
            theta_calc = node.boundary.width / abs(node_center_of_mass - self.r)
            if theta_calc < theta:
                line = drawLine(Point(self.r.x, self.r.y), Point(node_center_of_mass.x, node_center_of_mass.y), "blue")
                eraseLine(line)
                acceleration = calc_acceleration(self.r, node_center_of_mass, node.totalMass)
                print(acceleration)
                return "STUFF3"
                return acceleration # calculate acc from whole node

            else:

                self.check_theta(node.ne, theta)
                self.check_theta(node.nw, theta)
                self.check_theta(node.se, theta)
                self.check_theta(node.sw, theta)
        else:
            return "STUFF4"


    def add_acceleration(self, other):
        r = self.r - other.r
        r_squared = r * r

        # Calculate acceleration
        acc = -K1 * other.mass * r.unit / r_squared
        self.a = self.a + acc

    def add_acceleration_BH(self, node, theta_crit):
        acceleration = self.check_theta(node, theta_crit)
        assert acceleration
        if acceleration:
            self.a = self.a + acc
            print(acceleration)


    def add_acceleration_BH_BAD(self, node, theta_crit):

        # if node has not been created, ignore it
        if node is None:
            return

        # if node has no bodies, ignore it
        if node.totalMass == 0:
            return False

        # if node has a body that isn't the current body, calc acceleration due to other body and add it to current
        elif not node.isEmpty and not node.divided:
            other = node.bodies[0]

            # Calculate acceleration
            acc = calc_acceleration(self.r, other.r, other.mass)
            self.a = self.a + acc
            node.boundary.erase()
            return True


        # Finally, if node is internal, check if it has CoM far enough that all contained bodies can be
        # approximated as a single body (width of node is sufficiently small compared the distance of its CoM,
        # signified by theta_crit)
        else:
            node.boundary.draw(color="green")
            node_center_of_mass = (node.moment/node.totalMass)
            theta_calc = node.boundary.width / abs(node_center_of_mass - self.r)
            if theta_calc < theta_crit:
                # Calculate and add acceleration from node
                acc = calc_acceleration(self.r, node_center_of_mass, node.totalMass)
                self.a = self.a + acc
                return True

            else:
                node.boundary.erase()
                # Check children recursively until either node is external, or theta_calc < theta_crit
                self.add_acceleration_BH(node.nw, theta_crit)
                self.add_acceleration_BH(node.ne, theta_crit)
                self.add_acceleration_BH(node.sw, theta_crit)
                self.add_acceleration_BH(node.se, theta_crit)

    def update_pos(self, dt):
        self.r_0 = self.r
        self.r = self.r + (K2 * self.v * dt)
        self.v = self.v + (self.a * dt)

        print("*********", self.r - self.r_0)

        self.dot.move(self.r.x - self.r_0.x, self.r.y - self.r_0.y)

    def randomize(self, max_mass=1, max_r=1, max_v=1):
        m = max_mass #  * random.uniform(.01, 1)

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

        self.p1 = Point(self.x_center - self.width, self.y_center - self.height)
        self.p2 = Point(self.x_center - self.width, self.y_center + self.height)
        self.p3 = Point(self.x_center + self.width, self.y_center + self.height)
        self.p4 = Point(self.x_center + self.width, self.y_center - self.height)


        #self.rectangle = Rectangle(self.p1, self.p2)
        self.rectangle = Polygon(self.p1, self.p2, self.p3, self.p4)


    def contains(self, body):
        min_x = self.x_center - self.width
        max_x = self.x_center + self.width
        min_y = self.y_center - self.height
        max_y = self.y_center + self.height
        return (min_x < body.r.x < max_x) and (min_y < body.r.y < max_y)

    def draw(self, color="white"):
        self.rectangle.setOutline(color)
        try:
            self.rectangle.draw(WINDOW)
        except Exception as e:
            self.rectangle.undraw()
            self.rectangle.draw(WINDOW)

    def erase(self):
        self.rectangle.undraw()

    def intersects(self, range):
        return not (range.x_center - range.width > self.x_center + self.width) or \
                   (range.x_center + range.width < self.x_center - self.width) or \
                   (range.y_center - range.height > self.y_center + self.height) or \
                   (range.y_center + range.height < self.y_center - self.height)

    def __str__(self):
        out = f"=====CENTER: ({self.x_center, self.y_center})\n" + \
              f"====CORNERS: {self.p1, self.p2, self.p3, self.p4}\n"
        return out


class QuadTree:
    # Each node has 4 quadrants that may or may not be empty
    def __init__(self, boundary, capacity=1):
        self.capacity = capacity
        self.boundary = boundary
        self.bodies = []
        self.divided = False

        self.totalMass = 0
        self.moment = Vector3(0,0,0)

        #self.totalMass = 0
        #self.centerOfMass = Vector3(0,0,0)

        #self.nw = self.ne = self.sw = self.se = None

    @property
    def isEmpty(self):
        return len(self.bodies) == 0


    def subdivide(self):
        # When you successfully add a body to a child of the current node, current node total mass increases
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

        for q in [self.nw, self.ne, self.sw, self.se]:
            for body in self.bodies:
                #body.erase()
                if q.insert(body):
                    self.totalMass += body.mass
                    self.moment.x += body.mass * body.r.x
                    self.moment.y += body.mass * body.r.y
                    self.moment.z += body.mass * body.r.z


        self.bodies = []

        # nw.draw()
        # ne.draw()
        # sw.draw()
        # se.draw()

        self.divided = True

    def insert(self, body):

        # If body does not go within the bounds of this section, return
        if not (self.boundary.contains(body)):
            return False # body cannot be added

        # If there is space in this quad tree and if doesn't have subdivisions, add the object here
        if self.isEmpty and not self.divided:
            self.bodies.append(body)
            body.draw()
            return True

        # Otherwise, subdivide and then add the point to whichever node will accept it
        elif not self.divided:
            self.subdivide()
            # Need to re-insert all bodies that were already there
            # Try to add body to each child node and add to total mass

        for childQuad in [self.nw, self.ne, self.sw, self.se]:
            if childQuad.insert(body):
                self.totalMass += body.mass
                return True

        assert False, "MISSING A CONDITION"


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
        all_bodies = []
        for i in range(N):
            body = Body(index=i)
            body.randomize(max_mass=max_mass, max_r=max_r, max_v=max_v)
            self.insert(body)
            all_bodies.append(body)

        return all_bodies

    def populate_from_list(self, bodies):
        for body in bodies:
            body.dot.move(body.r.x - body.r_0.x, body.r.y - body.r_0.y)
            self.insert(body)

    def populate_twoBody(self):

        body_A = Body(mass=1, r=Vector3(-1,0,0), v=Vector3(0,-1,0), index=0)
        body_B = Body(mass=1, r=Vector3(1,0,0), v=Vector3(0,1,0), index=1)

        all_bodies = [body_A, body_B]
        for body in all_bodies:
            self.insert(body)
        return all_bodies

    def show(self):
        self.boundary.draw()
        if self.divided:
            self.nw.show()
            self.ne.show()
            self.sw.show()
            self.se.show()

    def erase(self):
        self.boundary.erase()

        if self.divided:
            self.nw.erase()
            self.ne.erase()
            self.sw.erase()
            self.se.erase()

    def query_select(self, x_center, y_center, w, h, show=False):
        qRange = Quadrant(x_center, y_center, w, h)

        bodies_found = self.query(qRange)

        if show:
            qRange.draw(color="red")
            for body in bodies_found:
                body.erase()
                body.size *= 10
                body.erase()
                body.draw(color="green")

        return len(bodies_found)




    def __str__(self):
        out = ""
        for att in vars(self):
            out += f"{att}: {self.__dict__[att]}\n"

        return out

    def __repr(self):
        return self.__str__()


