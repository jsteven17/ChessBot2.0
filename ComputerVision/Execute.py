import DetectBoard as detect
import numpy as np

userInput = ""
ROI =  np.float32([[0, 0], [0, 0], [0, 0], [0, 0]])

while(userInput != 'e'):
    userInput = input("Please enter a command: " )
    if(userInput == 'd'):
        ROI = detect.captureBoardCorners()
    if(userInput == 'm'):
        #Detect move
        print("Fuckass")
    