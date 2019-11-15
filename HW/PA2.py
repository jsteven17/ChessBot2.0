# Project_2
# Author: James Steven
# Date: 11/13/19

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from math import *

# DH TABLE
# +---+---+------+----+--------+
# |   | a |   α  |  d |    θ   |
# +---+---+------+----+--------+
# | 1 | 0 |   0  |  0 |   θ1   |
# +---+---+------+----+--------+
# | 2 | 0 | -90° | d2 | 90°+θ2 |
# +---+---+------+----+--------+
# | 3 | 0 |  90° | d3 |    0   |
# +---+---+------+----+--------+
# | 4 | 0 |   0  |  0 |   θ4   |
# +---+---+------+----+--------+
# | 5 | 0 | -90° |  0 | 90°+θ5 |
# +---+---+------+----+--------+
# | 6 | 0 |  90° |  0 |   θ6   |
# +---+---+------+----+--------+

#Set constants
d2 = 2

#Initialize user input variables
theta1 = -1000
theta2 = -1000
theta4 = -1000
theta5 = -1000
theta6 = -1000
d3 = -1000

# Get valid user input
while(theta1 < -180 or theta1 > 180):
    theta1 = int(input("Please enter Theta 1 [-180 180]: "))
while(theta2 < -90 or theta2 > 90):
    theta2 = int(input("Please enter Theta 2 [-90 90]: "))
while(d3 < 1 or d3 > 3):
    d3 = int(input("Please enter d3 [1 3]: "))
while(theta4 < -180 or theta4 > 180):
    theta4 = int(input("Please enter Theta 4 [-180 180]: "))
while(theta5 < -25 or theta5 > 25):
    theta5 = int(input("Please enter Theta 5 [-25 25]: "))
while(theta6 < -180 or theta6 > 180):
    theta6 = int(input("Please enter Theta 6 [-180 180]: "))

# Get 100 evenly spaced values from user input for animation
theta1s = np.linspace(0, theta1, 100)
theta2s = np.linspace(0, theta2, 100)
d3s = np.linspace(1, d3, 100)
theta4s = np.linspace(0, theta4, 100)
theta5s = np.linspace(0, theta5, 100)
theta6s = np.linspace(0, theta6, 100)
stepSizes = [theta1s, theta2s, d3s, theta4s, theta5s, theta6s]

#------------------THE FOLLOWING CODE ONLY PRINTS THE FINAL END EFFECTOR ORIENTATION----------------------

# Construct DH table
DH = [[0, 0, 0, radians(theta1)], [0, (-1*pi/2), d2, (pi/2) + radians(theta2)], [0, (pi/2), d3, 0], [0, 0, 0, radians(theta4)], [0, (-1*pi/2), 0, (pi/2) + radians(theta5)], [0, (pi/2), 0, radians(theta6)]]

# Calculate homogeneous transform matricies
T = []
for i in range(6):
    T.append([[cos(DH[i][3]), -1*sin(DH[i][3]), 0, DH[i][0]], [sin(DH[i][3])*cos(DH[i][1]), cos(DH[i][3])*cos(DH[i][1]), -1*sin(DH[i][1]), -1*DH[i][2]*sin(DH[i][1])], [sin(DH[i][3])*sin(DH[i][1]), cos(DH[i][3])*sin(DH[i][1]), cos(DH[i][1]), cos(DH[i][1])*DH[i][2]], [0, 0, 0, 1]])

# Decompose array into explicit homogeneous transformation matricies
T01 = np.array(T[0])
T12 = np.array(T[1])
T23 = np.array(T[2])
T34 = np.array(T[3])
T45 = np.array(T[4])
T56 = np.array(T[5])

# Assign Frames
Frame0 = [0, 0, 0, 1]

# Numpy frame
F0 = np.array(Frame0)

# Find transformation matricies from frame 0 to every other frame
H1 = np.array(T[0])
H2 = np.dot(H1, np.array(T[1]))
H3 = np.dot(H2, np.array(T[2]))
H4 = np.dot(H3, np.array(T[3]))
H5 = np.dot(H4, np.array(T[4]))
H6 = np.dot(H5, np.array(T[5]))

# Print final end effector position/orientation and transform matricies
print("\n")
print("Final end effector position and orientation matrix: ")
print(np.round(H5, 4))
print("\n")
print("T01: ")
print(np.round(T01, 4))
print("\n")
print("T12: ")
print(np.round(T12, 4))
print("\n")
print("T23: ")
print(np.round(T23, 4))
print("\n")
print("T34: ")
print(np.round(T34, 4))
print("\n")
print("T45: ")
print(np.round(T45, 4))
print("\n")
print("T56: ")
print(np.round(T56, 4))

#---------CONSTRUCT JACOBIAN AND CALCULATE VELOCITY KINEMATICS OF END EFFECTOR----

# Assign angular velocities to jacobian
w0 = H1[0:-1, 3]
w1 = H2[0:-1, 3]
w2 = 0
w3 = H4[0:-1, 3]
w4 = H5[0:-1, 3]
w5 = H6[0:-1, 3]

# Assign linear velocities to jacobian
v0 = np.cross(H1[0:-1, 3], H6[0:-1, 3])
v1 = np.cross(H2[0:-1, 3], (H6[0:-1, 3] - H1[0:-1, 3]))
v2 = H3[0:-1, 3]
v3 = np.cross(H4[0:-1, 3], (H6[0:-1, 3] - H3[0:-1, 3]))
v4 = np.cross(H5[0:-1, 3], (H6[0:-1, 3] - H4[0:-1, 3]))
v5 = np.cross(H6[0:-1, 3], (H6[0:-1, 3] - H5[0:-1, 3]))

# Construct jacobian
J = np.array([[v0, v1, v2, v3, v4, v5], [w0, w1, w2, w3, w4, w5]])

# Caculate qDot matrix from animation speed
qDot = []
for i in range(6):
    qDot.append((stepSizes[i][2]-stepSizes[i][1]) / .005)

print("\n")
print("qDOT:")
print(qDot)
print("\n")

# Find end effector linear and angular velocities
EElinear = np.dot(J[0,:], qDot)
EEangular = np.dot(J[1,:], qDot)

# Print jacobian and velocity dynamics of end effector
print("\n")
print("Jacobian: ")
print(J)
print("\n")
print("linear velocity of end effector: ")
print(np.round(EElinear, 4))
print("\n")
print("angular velocity of end effector: ")
print(np.round(EEangular, 4))

# --------THE FOLLOWING CODE SIMULATES MOVEMENT TO DESIRED JOINT POSITIONS--------

# Attaching 3D axis to the figure
simulation = plt.figure()
axis = p3.Axes3D(simulation)

# Setting the axes properties
axis.set_xlim3d([-5, 5])
axis.set_xlabel('X')
axis.set_ylim3d([-5, 5])
axis.set_ylabel('Y')
axis.set_zlim3d([0, 5])
axis.set_zlabel('Z')
axis.set_title('Project 2 Simulation')

def animate(frame):
    # Construct DH table with extra dummy links for simulation
    DH = [[0, 0, 3, radians(theta1s[frame])], [0, -pi/2, d2, pi/2 + radians(theta2s[frame])], [0, pi/2, d3s[frame], 0], [0, 0, 0, radians(theta4s[frame])], [0, -pi/2, 0, pi/2 + radians(theta5s[frame])], [0, pi/2, 0, radians(theta6s[frame])], [0, 0, .5, 0]]

    # Calculate transform matricies
    T = []
    for i in range(7):
        T.append([[cos(DH[i][3]), -1*sin(DH[i][3]), 0, DH[i][0]], [sin(DH[i][3])*cos(DH[i][1]), cos(DH[i][3])*cos(DH[i][1]), -1*sin(DH[i][1]), -1*DH[i][2]*sin(DH[i][1])], [sin(DH[i][3])*sin(DH[i][1]), cos(DH[i][3])*sin(DH[i][1]), cos(DH[i][1]), cos(DH[i][1])*DH[i][2]], [0, 0, 0, 1]])


    # Assign frames necessary to draw robot body
    Frame0 = np.array([0, 0, 0, 1])
    EEFrame1 = np.array([0, .3, 0, 1])
    EEFrame2 = np.array([0, -.3, 0, 1])
    EEFrame3 = np.array([0, .3, .2, 1])
    EEFrame4 = np.array([0, -.3, .2, 1])
    Frame0_2 = np.array([0, 0, 3, 1])

    # Find transformation matricies from frame 0 to every other frame
    H1 = np.array(T[0])
    H2 = np.dot(H1, np.array(T[1]))
    H3 = np.dot(H2, np.array(T[2]))
    H4 = np.dot(H3, np.array(T[3]))
    H5 = np.dot(H4, np.array(T[4]))
    H6 = np.dot(H5, np.array(T[5]))
    H7 = np.dot(H6, np.array(T[6]))

    # Multiply the RRPRRR starting position frames by their corresponding transformation matricies
    tFrame1 = np.dot(H2, Frame0)
    tFrame2 = np.dot(H6, Frame0)
    tFrame3 = np.dot(H7, Frame0)
    tEEFrame1 = np.dot(H7, EEFrame1)
    tEEFrame2 = np.dot(H7, EEFrame2)
    tEEFrame3 = np.dot(H7, EEFrame3)
    tEEFrame4 = np.dot(H7, EEFrame4)

    # Clear the plot
    axis.clear()

    # Set the axes
    axis.set_xlim3d([-5, 5])
    axis.set_xlabel('X')
    axis.set_ylim3d([-5, 5])
    axis.set_ylabel('Y')
    axis.set_zlim3d([0, 5])
    axis.set_zlabel('Z')
    axis.set_title('Project 2 Simulation')

    # Plot necessary line segments
    axis.plot([Frame0[0]], [Frame0[1]], [Frame0[2]], 'bo')
    axis.plot([Frame0[0], Frame0_2[0]],[Frame0[1], Frame0_2[1]],[Frame0[2], Frame0_2[2]], 'b')
    axis.plot([Frame0_2[0], tFrame1[0]],[Frame0_2[1], tFrame1[1]],[Frame0_2[2], tFrame1[2]], 'b')

    axis.plot([tFrame1[0]], [tFrame1[1]], [tFrame1[2]], 'go')
    axis.plot([tFrame1[0], tFrame2[0]],[tFrame1[1], tFrame2[1]],[tFrame1[2], tFrame2[2]], 'g')
 
    axis.plot([tFrame2[0]], [tFrame2[1]], [tFrame2[2]], 'ko')
    axis.plot([tFrame2[0], tFrame3[0]],[tFrame2[1], tFrame3[1]],[tFrame2[2], tFrame3[2]], 'k')

    axis.plot([tEEFrame1[0], tEEFrame2[0]],[tEEFrame1[1], tEEFrame2[1]],[tEEFrame1[2], tEEFrame2[2]], 'k')
    axis.plot([tEEFrame1[0], tEEFrame3[0]],[tEEFrame1[1], tEEFrame3[1]],[tEEFrame1[2], tEEFrame3[2]], 'k')
    axis.plot([tEEFrame4[0], tEEFrame2[0]],[tEEFrame4[1], tEEFrame2[1]],[tEEFrame4[2], tEEFrame2[2]], 'k')

# Run and save the simulation
simAnimation = animation.FuncAnimation(simulation, animate, frames = 100, interval = 5)
#simAnimation.save('Project_2_Simulation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()
