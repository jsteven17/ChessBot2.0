from math import *
import serial
import time

arduino = serial.Serial('COM5', 9600, timeout=.1)

# Function to calculate theta 1 and theta 2 based on desired end effector position, link lengths and angle constraints
# Assumes that theta 1 is already constrained to be on interval [0, pi]
def calcLinkAnglesForEndEffectorPosition(ee_X, ee_Y, ee_Z, theta1_Min, theta1_Max, theta2_Min, theta2_Max, L1, L2):
    alpha = acos((ee_X**2 + ee_Y**2 + L1**2 - L2**2) / (2 * L1 * sqrt(ee_X**2 + ee_Y**2)))
    beta = acos((L1**2 + L2**2 - ee_X**2 - ee_Y**2) / (2 * L1 * L2))
    gamma = atan2(ee_Y, ee_X)
    rightTheta1 = gamma - alpha
    rightTheta2 = pi - beta
    leftTheta1 = gamma + alpha
    leftTheta2 = beta - pi
    if(rightTheta1 > theta1_Min and rightTheta1 < theta1_Max and rightTheta2 > theta2_Min and rightTheta2 < theta2_Max):
        return rightTheta1, rightTheta2, ee_Z
    elif(leftTheta1 > theta1_Min and leftTheta1 < theta1_Max and leftTheta2 > theta2_Min and leftTheta2 < theta2_Max):
        return leftTheta1, leftTheta2, ee_Z
    else:
        raise Exception("There are no possible solutions")

x = input("Enter end effector x value: ")
y = input("Enter end effector y value: ")
z = input("Enter end effector z value: ")

t1, t2, z1 = calcLinkAnglesForEndEffectorPosition(int(x),int(y),int(z),-pi/2,pi/2,-1*pi,pi, 28.15, 23)

arduino.write("{:.3f},{:.3f},{:.3f}x".format(degrees(t1), degrees(t2), z1).encode())
time.sleep(.1)
print(arduino.read_all())
