import sys
from vector import *
from graphics import *
from physics_and_trees import *

from pyinstrument import Profiler

import time

class Simulation:
    def __init__(self):
        self.bodies = []
        self.win = None

    def setup(self):
        self.n = int(sys.argv[1])
        self.dt = float(sys.argv[2])

        # Initial parameters

        for i in range(self.n):
            body = Body(index=i)
            body.randomize(max_mass=1, max_r=10, max_v=0)
            self.bodies.append(body)

        self.win = setupWindow(900, 900, 10, 10)

        for body in self.bodies:
            body.draw(self.win)

    def update(self):

        for body in self.bodies:
            body.a = Vector3(0, 0, 0)
            for other in self.bodies:
                if other.index != body.index:
                    body.add_acceleration(other)
            # body.dot.undraw
            body.update_pos(self.dt)
            body.dot.move(body.r.x - body.r_0.x, body.r.y - body.r_0.y)


def setupWindow(x_pix_size, y_pix_size, xsize, ysize):
    win = GraphWin("NBody", x_pix_size, y_pix_size)
    win.setBackground("black")
    win.setCoords(-xsize, -ysize, xsize, ysize)
    return win



def main():
    profiler = Profiler()

    sim = Simulation()
    sim.setup()

    profiler.start()
    for i in range(100):
        sim.update()
    profiler.stop()
    print(profiler.output_text(unicode=True, color=True))

    #sim.win.getMouse()







if __name__ == "__main__":
    main()