import sys
from graphics import *
from vector import Vector3
from scipy.constants import G
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

    def __eq__(self, other):
        if isinstance(other, Body):
            return self.index == other.index
        elif isinstance(other, QuadTree):
            return len(other.query(other.boundary)) and abs(self.r - other.centerOfMass) < 0.001

    def draw(self, win, color="white"):
        #win.plot(self.r.x, self.r.y, "white")
        self.dot.setOutline(color)
        self.dot.draw(win)

    def erase(self):
        #win.plot(self.r.x, self.r.y, "black")
        self.dot.undraw()

    def add_acceleration(self, other):
        r = self.r - other.r
        r_squared = r * r

        # Calculate acceleration
        acc = -K1 * other.mass * r.unit / r_squared
        self.a = self.a + acc

    def add_acceleration_BH(self, node, theta_crit):

        """
        For each body b:
            For each node, (starting at root)
                if node is external (only 1 body):
                    calculate force between b and node body (RETURN)

                if node is internal (has children):
                    calculate theta = s/d (s = node.boundary.width, d = dist between body.r and node CoM)
                        ==> theta = node.boundary.width / abs(node.centerOfMass - r)
                    if theta < theta_crit, treat node as single body and calculate force (RETURN)
                    if theta > theta_crit, run procedure recursively on node's children
        """

        """
        SOMETHING IS WRONG WITH THIS ALGORITHM, NOT ACCURATELY DETECTING IF A BODY IS THE SAME AS ONE CONTAINED IN THE CURRENT NODE
        """


        if node is None:
            #print("Node is NONE")
            return False

        all_internal_bodies = node.query(node.boundary)

        if len(all_internal_bodies) == 0:
            return False

        elif len(all_internal_bodies) == 1 and self in all_internal_bodies:
            return False

        elif len(all_internal_bodies) == 1 and not (self in all_internal_bodies):
            other = node.bodies[0]
            r = self.r - other.r
            r_squared = r * r

            # Calculate acceleration
            acc = -K1 * other.mass * r.unit / r_squared
            self.a = self.a + acc
            return True


        # Finally, if node is not external, check if it has CoM far enough that all contained bodies can be
        # approximated as a single body (width of node is sufficiently small compared the distance of its CoM,
        # signified by theta_crit)
        else:

            totalMass = sum([body.mass for body in all_internal_bodies])
            # print(f"CoM: {node.calc_CenterOfMass()}")
            # print(f"Total mass: {totalMass}")
            # print(node.boundary)
            com_x = sum([body.r.x * body.mass for body in all_internal_bodies])
            com_y = sum([body.r.y * body.mass for body in all_internal_bodies])
            com_z = sum([body.r.z * body.mass for body in all_internal_bodies])
            centerOfMass = Vector3(com_x, com_y, com_z)/ totalMass

            theta_calc = node.boundary.width / abs(centerOfMass - self.r)
            #print(theta_calc, theta_crit)
            if theta_calc < theta_crit:
                #print(theta_calc, theta_crit, "APPROX NODE")
                # treat node bodies as single body
                r = self.r - centerOfMass
                r_squared = r * r

                # Calculate and add acceleration from node
                acc = -K1 * totalMass * r.unit / r_squared
                self.a = self.a + acc
                return True

            else:
                #print(theta_calc, theta_crit, "DON'T APPROX NODE - SPLIT")
                # Check children recursively until either node is external, or theta_calc < theta_crit
                self.add_acceleration_BH(node.nw, theta_crit)
                self.add_acceleration_BH(node.ne, theta_crit)
                self.add_acceleration_BH(node.sw, theta_crit)
                self.add_acceleration_BH(node.se, theta_crit)

    def update_pos(self, dt):
        #print(f"Body {self.index}")
        self.r_0 = self.r
        self.r = self.r + (K2 * self.v * dt)
        self.v = self.v + (self.a * dt)

        # print(f"a: {self.a}")
        # print(f"v: {self.v}")
        # print(f"r: {self.r}")

        #self.dot.move(self.r.x - self.r_0.x, self.r.y - self.r_0.y)

    def randomize(self, max_mass=1, max_r=1, max_v=1):
        m = max_mass  * random.uniform(.01, 1)

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

        self.p1_coords = [self.x_center - self.width, self.y_center - self.height]
        self.p2_coords = [self.x_center + self.width, self.y_center + self.height]

        p1 = Point(self.p1_coords[0], self.p1_coords[1])
        p2 = Point(self.p2_coords[0], self.p2_coords[1])

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

    def erase(self):
        self.rectangle.undraw()

    def intersects(self, range):
        return not (range.x_center - range.width > self.x_center + self.width) or \
                   (range.x_center + range.width < self.x_center - self.width) or \
                   (range.y_center - range.height > self.y_center + self.height) or \
                   (range.y_center + range.height < self.y_center - self.height)

    def __str__(self):
        out = f"====QUADRANT\n" + \
              f"=====CENTER: ({self.x_center, self.y_center})\n" + \
              f"====CORNERS: ({self.p1_coords[0], self.p1_coords[1]}), ({self.p2_coords[0], self.p2_coords[1]})\n"
        return out


class QuadTree:
    # Each node has 4 quadrants that may or may not be empty
    def __init__(self, boundary, capacity=1):
        self.capacity = capacity
        self.boundary = boundary
        self.bodies = []
        self.divided = False

        self.totalMass = 0
        self.centerOfMass = Vector3(0,0,0)

        #self.totalMass = 0
        #self.centerOfMass = Vector3(0,0,0)

        self.nw = self.ne = self.sw = self.se = None



    def calc_totalMass(self):
        all_bodies = self.query(self.boundary)
        return sum([body.mass for body in all_bodies])

    def calc_CenterOfMass(self):
        if self.totalMass == 0:
            return None
        else:
            x = sum([body.r.x * body.mass for body in self.query(self.boundary)])
            y = sum([body.r.y * body.mass for body in self.query(self.boundary)])
            z = sum([body.r.z * body.mass for body in self.query(self.boundary)])
            # print(f"N Nodies in Node: {len(self.query(self.boundary))} --- Total Mass of Node: {self.totalMass}")
            # print(f"CoM of Node: {Vector3(x, y, z)/ self.totalMass}")
            return Vector3(x, y, z)/ self.totalMass

    def isExternal(self):
        # Node is NOT external if it is divided. if it is not divided, it must have a body to be external
        if self.divided:
            return False
        elif len(self.query(self.boundary)) >= 1:
            return True

    # def isEmpty(self):
    #     # Node is NOT empty if it is divided. If it is not divided, it can't have any bodies to be empty
    #     if not self.divided and not (len(self.bodies) == 0):
    #         return True
    #     else:
    #         return True


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
            # print("Body out of bounds:")
            # print(f"Body:     {body.r}")
            # print(f"Boundary: {self.boundary.p1_coords, self.boundary.p2_coords}")
            return False

        # If number of bodies < capacity, append body to list of bodies
        # Else if capacity is full, subdivide
        if len(self.bodies) < self.capacity:
            self.bodies.append(body)
            self.totalMass += body.mass
            self.centerOfMass = self.centerOfMass + Vector3((body.r.x * body.mass)/self.totalMass,
                                                           (body.r.y * body.mass)/self.totalMass,
                                                           (body.r.z * body.mass)/self.totalMass)
            return True

        elif not self.divided:
            self.subdivide()

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

    def populate_random(self, win, N=10, max_mass=1, max_r=10, max_v=30):
        for i in range(N):
            body = Body(index=i)
            body.randomize(max_mass=max_mass, max_r=max_r, max_v=max_v)
            self.insert(body)
            body.draw(win)

    def populate_from_list(self, bodies, win):
        for body in bodies:
            self.insert(body)
            body.dot.move(body.r.x - body.r_0.x, body.r.y - body.r_0.y)

    def show(self, win):
        # print(f"({self.boundary.x_center},{self.boundary.y_center}) - N Bodies: {self.nBodies}")

        self.boundary.draw(win)

        if self.divided:
            self.nw.show(win)
            self.ne.show(win)
            self.sw.show(win)
            self.se.show(win)

    def erase(self):
        self.boundary.erase()

        if self.divided:
            self.nw.erase()
            self.ne.erase()
            self.sw.erase()
            self.se.erase()

    def query_select(self, win, x_center, y_center, w, h, show=False):
        qRange = Quadrant(x_center, y_center, w, h)

        bodies_found = self.query(qRange)

        if show:
            qRange.draw(win, color="red")
            for body in bodies_found:
                body.erase()
                body.size *= 10
                body.erase()
                body.draw(win, color="green")

        return len(bodies_found)




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