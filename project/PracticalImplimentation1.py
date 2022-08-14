import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
from pyfirmata import Arduino, SERVO, INPUT, OUTPUT, PWM
from time import sleep

port = '/dev/ttyUSB0'
try:
    Arduino_port = port
    pin = 10
    board = Arduino(Arduino_port)

    Motor1_IN1 = 7
    Motor1_IN2 = 8
    Motor2_IN1 = 5
    Motor2_IN2 = 4

    board.digital[Motor1_IN1].mode = OUTPUT
    board.digital[Motor1_IN2].mode = OUTPUT
    board.digital[Motor2_IN1].mode = OUTPUT
    board.digital[Motor2_IN2].mode = OUTPUT

except Exception as e:
    print(e)

try:
    def forward():
        board.digital[Motor1_IN1].write(1)
        board.digital[Motor1_IN2].write(0)
        board.digital[Motor2_IN1].write(1)
        board.digital[Motor2_IN2].write(0)

    def backward():
        board.digital[Motor1_IN1].write(0)
        board.digital[Motor1_IN2].write(1)
        board.digital[Motor2_IN1].write(0)
        board.digital[Motor2_IN2].write(1)

except Exception as e:
    print(e)

try:
    cap = cv2.VideoCapture(1)
    detector = htm.handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img, draw=False)
        if len(lmlist) != 0:
            x = lmlist[9][1]
            if x <= 320:
                forward()
            else:
                backward()
        cv2.imshow("Image", img)
        cv2.waitKey(1)

except KeyboardInterrupt:
    board.digital[Motor1_IN1].write(0)
    board.digital[Motor1_IN2].write(0)
    board.digital[Motor2_IN1].write(0)
    board.digital[Motor2_IN2].write(0)

except Exception as e:
    print(e)
