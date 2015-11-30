from __future__ import print_function
#List of files that will store image features
log1 = open("c:\\AsymmetryIndex.txt", "w")
log2 = open("c:\\CompactIndex.txt", "w")
log3 = open("c:\\DiameterIndex.txt", "w")
log4 = open("c:\\SolidityIndex.txt", "w")
log5 = open("c:\\ExtentIndex.txt", "w")
import os
import math
import numpy as np
import cv2
BLUE = [255,0,0]

#choose if train or test set
mypath = os.path.join('c:\\trainst')
#mypath = os.path.join('c:\\testSet')
images = list()
for item in os.listdir(mypath):
        image = cv2.imread(os.path.join(mypath, item))
        if image is not None:
            images.append(image)
            #resize image by half
            small = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
            constant= cv2.copyMakeBorder(small,3,3,3,3,cv2.BORDER_CONSTANT,value=BLUE)
            imgray = cv2.cvtColor(constant,cv2.COLOR_BGR2GRAY)
            contours, hierarchy = cv2.findContours(imgray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnt = contours[0]
            cv2.drawContours(constant, [cnt], 0, (50,50,100), 3)
            moments = cv2.moments(cnt)
            imgray1 = cv2.cvtColor(small,cv2.COLOR_BGR2GRAY)
            contours, hierarchy = cv2.findContours(imgray1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnt1 = contours[0]
            cv2.drawContours(small, [cnt1], 0, (255,55,0), 3)
            
            #area of lesion
            area = cv2.contourArea(cnt1)
            #area if image
            areaim = cv2.contourArea(cnt)
            #difference
            diff = areaim - area
            #asymmetry index
            asymmetryIndex = (diff/areaim)*100

            #calculate compactness
            perimeter = cv2.arcLength(cnt1,True)
            compactIndex = (perimeter**2)/(4*math.pi*area)

            #calculate Equivalent Diameter, which is the diameter of the circle whose area is same as the contour area.
            diameterIndex = np.sqrt(4*area/np.pi)

            #calculate Solidity, which is the ratio of contour area to its convex hull area.
            hull = cv2.convexHull(cnt1)
            hull_area = cv2.contourArea(hull)
            solidityIndex = float(area)/hull_area

            #calculate Extent, which is the ratio of contour area to bounding rectangle area.
            x,y,w,h = cv2.boundingRect(cnt1)
            rect_area = w*h
            extentIndex = float(area)/rect_area

            print("%.2f" % asymmetryIndex, file = log1)
            print("%.2f" % compactIndex, file = log2)
            print("%.2f" % diameterIndex, file = log3)
            print("%.2f" % solidityIndex, file = log4)
            print("%.2f" % extentIndex, file = log5)
