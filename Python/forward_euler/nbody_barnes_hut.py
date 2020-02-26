import sys
from vector import *
from graphics import *
from physics_and_trees import *
import random
import numpy as np
global N, dt
N = int(sys.argv[1])
dt = float(sys.argv[2])

class Simulation:

    def __init__(self, N, dt, theta=1.0, capacity=1, max_mass=1, max_r=10, max_v=30, window_x_size = 10, window_y_size=10):
        self.N = N
        self.dt = dt
        self.theta = theta
        self.capacity = capacity
        self.max_mass = max_mass
        self.max_r = max_r
        self.max_v = max_v
        self.win = None
        self.root = None
        self.active = False

        self.window_x_size = window_x_size
        self.window_y_size = window_y_size


    def setup(self):
        boundary = Quadrant(0, 0, self.window_x_size, self.window_y_size)
        self.root = QuadTree(boundary, capacity=self.capacity)
        self.root.populate_random(N=N, max_mass=self.max_mass, max_r=self.max_r, max_v=self.max_v)
        self.win = setupWindow(900, 900, self.window_x_size, self.window_x_size)
        self.root.show(self.win)
        self.win.getMouse()
        self.active = True

        print(f"Set up simulation with {self.query_select(0, 0, self.window_x_size, self.max_r)} bodies.")

        return self.active

    def query_select(self, x_center, y_center, w, h, show=False):
        qRange = Quadrant(x_center, y_center, w, h)

        bodies_found = self.root.query(qRange)

        if show:
            qRange.draw(self.win, color="red")
            for body in bodies_found:
                body.erase(self.win)
                body.size *= 10
                body.draw(self.win, color="green")

        return len(bodies_found)
        self.win.getMouse()

    def update(self):
        # gets called each frame/time step

        # All bodies must include bodies outside of window range
        all_space = Quadrant(0, 0, 1000*self.window_x_size, 1000*self.window_y_size)
        all_bodies = self.root.query(all_space)
        #print(len(all_bodies))
        # print(self.root.totalMass)
        # print(self.root.centerOfMass)

        for body in all_bodies:
            body.a = Vector3(0,0,0) # New frame, start adding accelerations from other bodies/nodes at zero
            body.add_acceleration_BH(self.root, self.theta) # This function will step through tree recursively, adding to body.a
            body.update_pos(self.dt) # body now has up-to-date acceleration, so update position and move the dot

        #self.win.getMouse()

    def end(self):
        self.win.getMouse()
        self.active = False

    def run_simulation(self):
        assert self.setup()
        try:
            while self.active:
                self.update()
        except KeyboardInterrupt:
            self.end()




    # ========================================================================

    """
    For each body b:
        For each node, (starting at root)
            if node is external (only 1 body):
                calculate force between b and node body (RETURN)

            if node is internal (has children):
                calculate s/d (s = node.boundary.width, d = dist between body.r and node CoM)
                    s/d = node.boundary.width / abs(node.centerOfMass - r)
                if s/d < theta, treat node as single body and calculate force (RETURN)
                if s/d > theta, run procedure recursively on node's children
    draft: 

    def add_acceleration_BH(self, node):

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

            elif s_d >= theta:
                self.add_acceleration(node.nw)
                self.add_acceleration(node.ne)
                self.add_acceleration(node.sw)
                self.add_acceleration(node.se)


    """


def main():
    sim = Simulation(N, dt, max_r=10, max_v=0, theta=0.5)
    sim.run_simulation()


if __name__ == "__main__":
    main()