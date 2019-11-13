import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from math import *

# Joint constants
a1 = 5
a2 = 25
a3 = 5
a4 = 25
d0 = 40

# Get user input
theta1 = int(input("Please enter Theta 1: "))
theta2 = int(input("Please enter Theta 2: "))
d1 = int(input("Please enter d1: "))

# Get 100 evenly spaced values from user input for animation
theta1s = np.linspace(0, theta1, 100)
theta2s = np.linspace(0, theta2, 100)
d1s = np.linspace(d0, d1, 100)

# Attaching 3D axis to the figure
simulation = plt.figure()
axis = p3.Axes3D(simulation)

# Setting the axes properties
axis.set_xlim3d([0, 100])
axis.set_xlabel('X')
axis.set_ylim3d([-100, 100])
axis.set_ylabel('Y')
axis.set_zlim3d([0, 100])
axis.set_zlabel('Z')
axis.set_title('Chess SCARA Simulation')

def animate(frame):
    # Construct DH table
    DH = [[0, 0, d1s[frame], 0], [a1, 0, 0, 0], [a2, 0, 0, radians(theta1s[frame])], [0, 0, -1 * a3, 0], [a4, 0, 0, radians(theta2s[frame])]]

    # Calculate transform matricies
    T = []
    for i in range(5):
        T.append([[cos(DH[i][3]), -1*sin(DH[i][3])*cos(DH[i][1]), sin(DH[i][3])*sin(DH[i][1]), DH[i][0]*cos(DH[i][3])], [sin(DH[i][3]), cos(DH[i][3])*cos(DH[i][1]), -1*cos(DH[i][3])*sin(DH[i][1]), DH[i][0]*sin(DH[i][3])], [0, sin(DH[i][1]), cos(DH[i][1]), DH[i][2]], [0, 0, 0, 1]])


    # Assign origin frame
    F0 = np.array([0, 0, 0, 1])

    # Find transformation matricies from frames 0 to 1, 0 to 2, and 0 to 3
    H0 = np.array(T[0])
    H1 = np.dot(H0, np.array(T[1]))
    H2 = np.dot(H1, np.array(T[2]))
    H3 = np.dot(H2, np.array(T[3]))
    H4 = np.dot(H3, np.array(T[4]))

    # Multiply the SCARA starting position frames by their corresponding transformation matricies
    tFrame1 = np.dot(H0, F0)
    tFrame2 = np.dot(H1, F0)
    tFrame3 = np.dot(H2, F0)
    tFrame4 = np.dot(H3, F0)
    tFrame5 = np.dot(H4, F0)

    # Clear the plot
    axis.clear()

    # Set the axes

    axis.set_xlim3d([0, 100])
    axis.set_xlabel('X')
    axis.set_ylim3d([-100, 100])
    axis.set_ylabel('Y')
    axis.set_zlim3d([0, 100])
    axis.set_zlabel('Z')
    axis.set_title('Chess SCARA Simulation')

    # Plot each of the 5 required line segments
    axis.plot([F0[0], tFrame1[0], tFrame2[0]],[F0[1], tFrame1[1], tFrame2[1]],[F0[2], tFrame1[2], tFrame2[2]], '-o',)
    axis.plot([tFrame2[0], tFrame3[0]],[tFrame2[1], tFrame3[1]],[tFrame2[2], tFrame3[2]], '-o',)
    axis.plot([tFrame3[0], tFrame4[0]],[tFrame3[1], tFrame4[1]],[tFrame3[2], tFrame4[2]], '-o',)
    axis.plot([tFrame4[0], tFrame5[0]],[tFrame4[1], tFrame5[1]],[tFrame4[2], tFrame5[2]], '-o',)

# Run and save the simulation
simAnimation = animation.FuncAnimation(simulation, animate, frames = 100, interval = 5)
simAnimation.save('SCARA_Simulation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()