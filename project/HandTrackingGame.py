import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


cap = cv2.VideoCapture(1)
detector = htm.handDetector()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist) != 0:
        print(lmlist[0])

    cv2.imshow("Image", img)
    cv2.waitKey(1)
