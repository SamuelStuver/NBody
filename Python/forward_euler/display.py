from graphics import *

def setupWindow(x_pix_size, y_pix_size, xsize=10, ysize=10):
    win = GraphWin("NBody", x_pix_size, y_pix_size)
    win.setBackground("black")
    win.setCoords(-xsize, -ysize, xsize, ysize)
    return win


WINDOW = setupWindow(800, 800)
