import sys
from vector import *
from graphics import *
from physics_and_trees import *

import time

def setupWindow(x_pix_size, y_pix_size, xsize, ysize):
    win = GraphWin("NBody", x_pix_size, y_pix_size)
    win.setBackground("black")
    win.setCoords(-xsize, -ysize, xsize, ysize)
    return win

def main():

    n = int(sys.argv[1])
    dt = float(sys.argv[2])

    # Initial parameters

    bodies = []
    for i in range(n):
        body = Body(index=i)
        body.randomize(max_mass=1, max_r=10, max_v=0)
        bodies.append(body)

    win = setupWindow(900, 900, 10, 10)
    t = 0

    for body in bodies:
        body.draw(win)

    try:
        while True:

            for body in bodies:
                body.a = Vector3(0,0,0)
                for other in bodies:
                    if other.index != body.index:
                        body.add_acceleration(other)
                #body.dot.undraw
                body.update_pos(dt)
                #body.draw(win)

            t += dt
    except KeyboardInterrupt:
        win.getMouse()  # pause for click in window





if __name__ == "__main__":
    main()