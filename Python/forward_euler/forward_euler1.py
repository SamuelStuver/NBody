import matplotlib
import sys
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pprint as pp
import time

def mag(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    


def main():

    dt = float(sys.argv[1])

    # Initial relative position
    r_0 = [1, 0, 0]
    v_0 = [0, 0.5, 0]

    r_list = [r_0]
    v_list = [v_0]

    t = 0

    r = r_0
    v = v_0

    while t < 10:
        r_squared = (r[0]**2 + r[1]**2 + r[2]**2)
        # Calculate current acceleration
        a = [0,0,0]
        for k in range(3): 
            a[k] = -r[k] / (r_squared * math.sqrt(r_squared))
        # Calcuate new position and velocity based on calculated acceleration
        for k in range(3): 
            r[k] += v[k] * dt
            v[k] += a[k] * dt
        print(mag(r), mag(v))
        
       
        r_list.append(r)
        v_list.append(v)
        

        t += dt
    
    # for i in r_list:
    #     print(i)



if __name__ == "__main__":
    main()