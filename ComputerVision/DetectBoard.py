import cv2
import time
from matplotlib import pyplot as plt
import numpy as np
import math

def captureBoardCorners():
    cam = cv2.VideoCapture(0)
    chessboardTemplate = cv2.imread('GeneratedChessTemplate.jpg')

    for i in range(10):
        ret, image = cam.read()

    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equ = cv2.equalizeHist(grey)
    edges = cv2.Canny(equ,50,300)
    imageUnique = image.copy()
    ROIs = image.copy()
    origImage = image.copy()

    height = image.shape[0]
    width = image.shape[1]

    # plt.subplot(121),plt.imshow(equ,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()

    lines = cv2.HoughLines(edges, 1, np.pi / 180, 100, 20, 10)

    distThresh = .1
    angleThresh = .01
    storedLines = []
    vertLines = []
    horizLines = []
    verteces = []
    uLeft = []
    uRight = []
    bLeft = []
    bRight = []
    potROIPts = []
    currMin = 0

    if lines is not None:
        #Find good candidate vertical and horizontal lines using thresholds
        #Store canditates separately
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(image, pt1, pt2, (0,255,0), 1)
            unique = True
            if(theta>1 and theta<2 or theta>0 and theta<.2 or theta>2.8 and theta<3.2):
                for storedLine in storedLines:
                    sRho, sTheta, sX0, sY0 = storedLine
                    if((abs(rho-sRho)/sRho < distThresh) and (abs(theta-sTheta)/sTheta < angleThresh)):
                        unique = False
                    if(abs(sTheta-theta) < 0.1):
                        if((math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta)) == 0):
                            b = 0
                        else:
                            b = ((sY0-y0)*math.sin(theta) + (sX0-x0)*math.cos(theta)) / (math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta))
                        xIntersect = sX0 - b*math.sin(sTheta)
                        yIntersect = sY0 + b*math.cos(sTheta)
                        if(xIntersect>0 and xIntersect<height and yIntersect>0 and yIntersect<width):
                            unique = False
                if unique:
                    t = (rho, theta, x0, y0)
                    storedLines.append(t)
                    if(theta>1 and theta<2):
                        horizLines.append(t)
                    elif(theta>0 and theta<.2 or theta>2.8 and theta<3.2):
                        vertLines.append(t)

        #Calculate all vertical and horizontal line intersections
        for hLine in horizLines:
            for vLine in vertLines:
                sRho, sTheta, sX0, sY0 = vLine
                rho, theta, x0, y0 = hLine
                if((math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta)) == 0):
                    b = 0
                else:
                    b = ((sY0-y0)*math.sin(theta) + (sX0-x0)*math.cos(theta)) / (math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta))
                xIntersect = sX0 - b*math.sin(sTheta)
                yIntersect = sY0 + b*math.cos(sTheta)
                t = (xIntersect, yIntersect)
                verteces.append(t)

        #Calculate all line intersections with top and left border of image
        verticalIntersections = []
        for i in range(0, len(vertLines)):
            sRho, sTheta, sX0, sY0 = vertLines[i]
            theta = math.pi/2
            rho, x, y = 0, 0, 0
            if((math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta)) == 0):
                b = 0
            else:
                b = ((sY0-y)*math.sin(theta) + (sX0-x)*math.cos(theta)) / (math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta))
            xIntersect = sX0 - b*math.sin(sTheta)
            verticalIntersections.append(xIntersect)

        horizontalIntersections = []
        for i in range(0, len(horizLines)):
            sRho, sTheta, sX0, sY0 = horizLines[i]
            theta = math.pi
            rho, x, y = 0, 0, 0
            if((math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta)) == 0):
                b = 0
            else:
                b = ((sY0-y)*math.sin(theta) + (sX0-x)*math.cos(theta)) / (math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta))
            yIntersect = sY0 + b*math.cos(sTheta)
            horizontalIntersections.append(yIntersect)

        #Calculate all potential line pairs greater than threshold value
        threshold = 0.60
        horizPairs = []
        for i in range(0,len(horizontalIntersections)):
            for j in range(i, len(horizontalIntersections)):
                if(abs(horizontalIntersections[i] - horizontalIntersections[j]) / width > threshold):
                    if(horizontalIntersections[i] < horizontalIntersections[j]):
                        t = (i,j)
                    else:
                        t = (j,i)
                    horizPairs.append(t)
        vertPairs = []
        for i in range(0,len(verticalIntersections)):
            for j in range(i, len(verticalIntersections)):
                if(abs(verticalIntersections[i] - verticalIntersections[j]) / height > threshold):
                    if(verticalIntersections[i] < verticalIntersections[j]):
                        t = (i,j)
                    else:
                        t = (j,i)
                    vertPairs.append(t)

        #Calculate all ROI square corners (store as list of list of verteces)
        ROIVerteces = []
        for i in range(0, len(horizPairs)):
            for j in range(0, len(vertPairs)):
                pts = []
                for k in range(0, 2):
                    for m in range(0, 2):
                        sRho, sTheta, sX0, sY0 = horizLines[horizPairs[i][k]]
                        rho, theta, x0, y0 = vertLines[vertPairs[j][m]]
                        if((math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta)) == 0):
                            b = 0
                        else:
                            b = ((sY0-y0)*math.sin(theta) + (sX0-x0)*math.cos(theta)) / (math.cos(theta)*math.sin(sTheta) - math.cos(sTheta)*math.sin(theta))
                        xIntersect = sX0 - b*math.sin(sTheta)
                        yIntersect = sY0 + b*math.cos(sTheta)
                        pt = (int(xIntersect), int(yIntersect))
                        pts.append(pt)
                ROIVerteces.append(pts)

        #Draw all ROI squares
        i=0
        potROIImgs = []
        for squareList in ROIVerteces:
            p0x, p0y = squareList[0]
            p1x, p1y = squareList[1]
            p2x, p2y = squareList[2]
            p3x, p3y = squareList[3]
            pts = np.float32([[p0x, p0y], [p1x, p1y], [p2x, p2y], [p3x, p3y]])
            ptsTarget = np.float32([[0, 0], [400, 0], [0, 400], [400, 400]])
            cv2.line(ROIs, squareList[0], squareList[1], (255,255,0), 1)
            cv2.line(ROIs, squareList[1], squareList[3], (255,255,0), 1)
            cv2.line(ROIs, squareList[3], squareList[2], (255,255,0), 1)
            cv2.line(ROIs, squareList[2], squareList[0], (255,255,0), 1)

            perspTransformMat = cv2.getPerspectiveTransform(pts, ptsTarget)
            perspTransResult = cv2.warpPerspective(origImage, perspTransformMat, (400, 400))
            potROIImgs.append(perspTransResult)
            potROIPts.append(pts)
            #cv2.imwrite("Potential_ROI_{}.png".format(i), perspTransResult)
            i = i+1

        #Find ROI with lowest SAD
        diff = cv2.absdiff(potROIImgs[0], chessboardTemplate)
        minMean = np.mean(diff)
        for i in range(0, len(potROIImgs)):
            diff = cv2.absdiff(potROIImgs[i], chessboardTemplate, diff)
            #cv2.imwrite("diff_{}.png".format(i), diff)
            if(np.mean(diff) < minMean):
                minMean = np.mean(diff)
                currMin = i
        cv2.imwrite("C:/Users/James/Chess Robot/ComputerVision/PerspectiveTransImages/trasformedBoard.png", potROIImgs[currMin])

        #Bisect into 64 squares
        for i in range(0, 8):
            for j in range(0, 8):
                temp = cv2.imread("C:/Users/James/Chess Robot/ComputerVision/PerspectiveTransImages/trasformedBoard.png")
                cropped = temp[(i*50):(i*50 + 50), (j*50):(j*50 + 50)]
                cv2.imwrite("C:/Users/James/Chess Robot/ComputerVision/BisectedImages/{}_{}.png".format(i, j), cropped)

        #******************WRITE A BUNCH OF STUFF TO IMGS**********************
        a = math.cos(math.pi/2)
        b = math.sin(math.pi/2)
        x0 = a * 0
        y0 = b * 0
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv2.line(imageUnique, pt1, pt2, (255,100,100), 10)

        a = math.cos(math.pi)
        b = math.sin(math.pi)
        x0 = a * 0
        y0 = b * 0
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv2.line(imageUnique, pt1, pt2, (255,100,100), 10)

        for vertex in verteces:
            x, y = vertex
            if(x > width/2 and y > height/2):
                bRight.append(vertex)
            elif(x < width/2 and y > height/2):
                bLeft.append(vertex)
            elif(x > width/2 and y < height/2):
                uRight.append(vertex)
            elif(x < width/2 and y < height/2):
                uLeft.append(vertex)

        for vertex in uLeft:
            x, y = vertex
            cv2.circle(imageUnique, (int(x), int(y)), 4, (0,255,0), 2)
        for vertex in uRight:
            x, y = vertex
            cv2.circle(imageUnique, (int(x), int(y)), 4, (255,0,0), 2)
        for vertex in bLeft:
            x, y = vertex
            cv2.circle(imageUnique, (int(x), int(y)), 4, (0,0,255), 2)
        for vertex in bRight:
            x, y = vertex
            cv2.circle(imageUnique, (int(x), int(y)), 4, (255,255,255), 2)

        for i in range(0, len(storedLines)):
            rho, theta, x0, y0 = storedLines[i]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            if(storedLines[i] in horizLines):
                cv2.line(imageUnique, pt1, pt2, (255,255,0), 1)
            else:
                cv2.line(imageUnique, pt1, pt2, (255,0,255), 1)


    cv2.imwrite("edges.png", edges)
    cv2.imwrite("equalized.png", equ)
    cv2.imwrite("hough.png", image)
    cv2.imwrite("houghUnique.png", imageUnique)
    cv2.imwrite("ROIs.png", ROIs)

    cam.release()
    cv2.destroyAllWindows()
    
    return potROIPts[currMin]

def bisectChessboard(ROI, chessboard):
    #Bisect into 64 squares
    for i in range(0, 8):
        for j in range(0, 8):
            cropped = chessboard[(i*50):(i*50 + 50), (j*50):(j*50 + 50)]
            cv2.imwrite("C:/Users/James/Chess Robot/ComputerVision/BisectedImages/{}_{}.png".format(i, j), cropped)