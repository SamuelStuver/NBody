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

    def __init__(self, N, dt, theta=1.0, capacity=1, max_mass=1, max_r=10, max_v=30, window_x_size = 10, window_y_size=10, show_nodes=False):
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
        self.max_width_or_height = self.window_x_size = self.window_y_size = window_x_size
        self.show_nodes = show_nodes
        self.all_bodies = []

    def setup(self):
        self.win = setupWindow(900, 900, self.window_x_size, self.window_x_size)
        boundary = Quadrant(0, 0, self.window_x_size, self.window_y_size)
        self.root = QuadTree(boundary, capacity=self.capacity)
        self.all_bodies = self.root.populate_random(self.win, N=N, max_mass=self.max_mass, max_r=self.max_r, max_v=self.max_v) # DRAW EACH BODY UPON INSERT

        # Optional, modify max_x_coord and max_y_coord based on bodies with highest x and y

        print(f"Set up simulation with {self.query_select(0, 0, self.window_x_size, self.max_r)} bodies.")

        self.root.show(self.win)

        self.win.getMouse()
        self.root.erase()
        self.active = True


        return self.active



    def update(self):
        # gets called each frame/time step
        # For each body out of total:
            # set acceleration of body to zero
            # Add acceleration from other bodies or nodes based on B-H Algorithm
            # Update the coordinates of the body
        # Determine the highest and lowest x and y coordinates of any body
        # New root node boundary is Quadrant((max_x_coord + min_x_coord)/2, (max_y_coord + min_y_coord)/2, (max_x_coord - min_x_coord)/2, (max_y_coord - min_y_coord)/2)
        # Populate new QuadTree with updated bodies (QuadTree()) # ERASE AND RE-DRAW EACH BODY UPON INSERT



        for body in self.all_bodies:
            body.a = Vector3(0,0,0) # New frame, start adding accelerations from other bodies/nodes at zero
            body.add_acceleration_BH(self.root, self.theta) # This function will step through tree recursively, adding to body.a
            body.update_pos(self.dt) # body now has up-to-date acceleration, so update position and move the dot
            # If a new body has an x or y value greater than the current max, update the current max
            if body.r.x > self.max_width_or_height:
                self.max_width_or_height = body.r.x
            if body.r.y > self.max_width_or_height:
                self.max_width_or_height = body.r.y
        boundary = Quadrant(0, 0, self.max_width_or_height, self.max_width_or_height)
        self.root = QuadTree(boundary, capacity=self.capacity)
        self.root.populate_from_list(self.all_bodies) # ERASE AND RE-DRAW EACH BODY UPON INSERT

        if self.show_nodes:
            self.root.show(self.win)
            self.root.erase()


        #self.win.getMouse()
        return self.win

    def end(self):
        self.win.getMouse()
        self.active = False

    def run_simulation(self):
        assert self.setup()
        try:
            while self.active:
                win = self.update()

        except KeyboardInterrupt:
            self.end()


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
    sim = Simulation(N, dt, max_r=10, max_v=1, theta=1, show_nodes=False)
    sim.run_simulation()


if __name__ == "__main__":
    main()