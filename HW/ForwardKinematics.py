import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from math import *

# Joint constants
a1 = 2
a2 = 2
d1 = 2

# Get user input
theta1 = int(input("Please enter Theta 1: "))
theta2 = int(input("Please enter Theta 2: "))
d3 = int(input("Please enter d3: "))

# Get 100 evenly spaced values from user input for animation
theta1s = np.linspace(0, theta1, 100)
theta2s = np.linspace(0, theta2, 100)
d3s = np.linspace(0, d3, 100)

# Attaching 3D axis to the figure
simulation = plt.figure()
axis = p3.Axes3D(simulation)

# Setting the axes properties
axis.set_xlim3d([-10, 10])
axis.set_xlabel('X')
axis.set_ylim3d([-10, 10])
axis.set_ylabel('Y')
axis.set_zlim3d([-10, 10])
axis.set_zlabel('Z')
axis.set_title('SCARA Simulation')

def animate(frame):
    # Construct DH table
    DH = [[a1, 0, d1, radians(theta1s[frame])], [a2, pi, 0, radians(theta2s[frame])], [0, 0, d3s[frame], 0]]

    # Calculate transform matricies
    T = []
    for i in range(3):
        T.append([[cos(DH[i][3]), -1*sin(DH[i][3])*cos(DH[i][1]), sin(DH[i][3])*sin(DH[i][1]), DH[i][0]*cos(DH[i][3])], [sin(DH[i][3]), cos(DH[i][3])*cos(DH[i][1]), -1*cos(DH[i][3])*sin(DH[i][1]), DH[i][0]*sin(DH[i][3])], [0, sin(DH[i][1]), cos(DH[i][1]), DH[i][2]], [0, 0, 0, 1]])


    # Assign Frames
    Frame0 = [0, 0, 0, 1]
    Frame1 = [0, 0, d1, 1]
    Frame2 = [a1, 0, d1, 1]
    Frame3 = [a1 + a2, 0, d1, 1]
    Frame4 = [a1 + a2, 0, d1, 1]

    # Numpy frames
    F0 = np.array(Frame0)
    F1 = np.array(Frame1)
    F2 = np.array(Frame2)
    F3 = np.array(Frame3)
    F4 = np.array(Frame4)

    # Find transformation matricies from frames 0 to 1, 0 to 2, and 0 to 3
    H0 = np.array(T[0])
    H1 = np.dot(H0, np.array(T[1]))
    H2 = np.dot(H1, np.array(T[2]))

    # Multiply the SCARA starting position frames by their corresponding transformation matricies
    tFrame2 = np.dot(H0, F0)
    tFrame3 = np.dot(H1, F0)
    tFrame4 = np.dot(H2, F0)

    # Clear the plot
    axis.clear()

    # Set the axes
    axis.set_xlim3d([-10, 10])
    axis.set_xlabel('X')
    axis.set_ylim3d([-10, 10])
    axis.set_ylabel('Y')
    axis.set_zlim3d([-10, 10])
    axis.set_zlabel('Z')
    axis.set_title('SCARA Simulation')

    # Plot each of the 4 required line segments
    axis.plot([Frame0[0], Frame1[0]],[Frame0[1], Frame1[1]],[Frame0[2], Frame1[2]], '-o',)
    axis.plot([Frame1[0], tFrame2[0]],[Frame1[1], tFrame2[1]],[Frame1[2], tFrame2[2]], '-o',)
    axis.plot([tFrame2[0], tFrame3[0]],[tFrame2[1], tFrame3[1]],[tFrame2[2], tFrame3[2]], '-o',)
    axis.plot([tFrame3[0], tFrame4[0]],[tFrame3[1], tFrame4[1]],[tFrame3[2], tFrame4[2]], '-o',)

# Run and save the simulation
simAnimation = animation.FuncAnimation(simulation, animate, frames = 100, interval = 5)
simAnimation.save('SCARA_Simulation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()

#------------------THE FOLLOWING CODE ONLY PRINTS THE FINAL END EFFECTOR ORIENTATION----------------------

# Construct DH table
DH = [[a1, 0, d1, radians(theta1)], [a2, pi, 0, radians(theta2)], [0, 0, d3, 0]]

# Calculate transform matricies
T = []
for i in range(3):
    T.append([[cos(DH[i][3]), -1*sin(DH[i][3])*cos(DH[i][1]), sin(DH[i][3])*sin(DH[i][1]), DH[i][0]*cos(DH[i][3])], [sin(DH[i][3]), cos(DH[i][3])*cos(DH[i][1]), -1*cos(DH[i][3])*sin(DH[i][1]), DH[i][0]*sin(DH[i][3])], [0, sin(DH[i][1]), cos(DH[i][1]), DH[i][2]], [0, 0, 0, 1]])

# Assign Frames
Frame0 = [0, 0, 0, 1]

# Numpy frame
F0 = np.array(Frame0)

# Find transformation matricies from frames 0 to 1, 0 to 2, and 0 to 3
H0 = np.array(T[0])
H1 = np.dot(H0, np.array(T[1]))
H2 = np.dot(H1, np.array(T[2]))

# Print final end effector position/orientation
print("Final end effector position and orientation matrix: \n")
print(H2)
print("\n")
print(np.array(T[0]))
print("\n")
print(np.array(T[1]))
print("\n")
print(np.array(T[2]))