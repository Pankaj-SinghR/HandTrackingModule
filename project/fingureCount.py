import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(1)
cap.set(3, wCam) # setting width 
cap.set(4, hCam) # setting height

detector = htm.handDetector()

while True:
    success, img  = cap.read()
    
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    print(lmList)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
