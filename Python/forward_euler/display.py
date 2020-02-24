from graphics import *

# def main():
#     win = GraphWin("NBody", 500, 500)
#     win.setBackground("black")
#     win.plot(250, 250, "white")
#     win.getMouse()  # pause for click in window
#     win.close()
#
# main()


def setupWindow(xsize, ysize):
    win = GraphWin("NBody", 500, 500)
    win.setBackground("black")
    return win