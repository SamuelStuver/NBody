import sys
from vector import *
from graphics import *
from physics_and_trees import *
import random
import numpy as np


def main():
    N = int(sys.argv[1])

    max_r = 10
    max_v = 30
    max_mass = 1
    capacity = 1

    boundary = Quadrant(0, 0, max_r, max_r)
    qTree = QuadTree(boundary, capacity=capacity)
    qTree.populate_random(N=N, max_mass=1, max_r=10, max_v=30)


    win = setupWindow(900, 900, 10, 10)
    #qTree.show(win)
    #win.getMouse()

    # for i in range(5):
    #     qRange = Quadrant(random.uniform(-10,10), random.uniform(-10,10), 2, 2)
    #     qRange.draw(win, color="red")
    #     print(f"Range has {len(qTree.query(qRange))} bodies")
    #     for body in qTree.query(qRange):
    #         body.erase(win)
    #         body.size *= 10
    #         body.draw(win, color="red")
    #     win.getMouse()

    # ========================================================================
    t = 0
    dt = 0.01
    try:
        while t < 1:
            print(f"t: {t}")
            for body in qTree.bodies:
                body.a = Vector3(0,0,0)
                body.add_acceleration_BH(qTree)

            body.update(dt)

            t += dt
    except KeyboardInterrupt:
        win.getMouse()  # pause for click in window

    win.getMouse()  # pause for click in window

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



if __name__ == "__main__":
    main()