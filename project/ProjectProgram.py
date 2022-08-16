import cv2
import mediapipe as mp
from time import sleep
import HandTrackingModule as htm
from pyfirmata import Arduino, SERVO, INPUT, OUTPUT, PWM
from time import sleep

port = '/dev/ttyUSB0'
try:
    Arduino_port = port
    board = Arduino(Arduino_port)
    track_angle = 115

    Motor1_IN1 = 7
    Motor1_IN2 = 8
    Motor2_IN1 = 5
    Motor2_IN2 = 4
    Servo_Pin  = 10

    board.digital[Motor1_IN1].mode = OUTPUT
    board.digital[Motor1_IN2].mode = OUTPUT
    board.digital[Motor2_IN1].mode = OUTPUT
    board.digital[Motor2_IN2].mode = OUTPUT
    board.digital[Servo_Pin].mode  = SERVO
    board.digital[Servo_Pin].write(115)

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

    def stop_motor():
        board.digital[Motor1_IN1].write(0)
        board.digital[Motor1_IN2].write(0)
        board.digital[Motor2_IN1].write(0)
        board.digital[Motor2_IN2].write(0)

    def left_rotate(angle):
        board.digital[Servo_Pin].write(angle)
        sleep(0.015)

    def right_rotate(angle):
        board.digital[Servo_Pin].write(angle)
        sleep(0.015)

except Exception as e:
    print(e)

try:
    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(1)
    cap.set(3, wCam) # setting width 
    cap.set(4, hCam) # setting height
    detector = htm.handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img, draw=False)
        
        if len(lmlist) != 0:

            x = lmlist[9][1]
            y = lmlist[9][2]
            # print(x, y)
# and (lmlist[12][2] > lmlist[10][2]) and (lmlist[16][2] > lmlist[14][2])and (lmlist[20][2] > lmlist[18][2]) and (lmlist[4][2] > lmlist[3][2])
            if (lmlist[8][2] > lmlist[6][2] ): # this will stop the motor if you make a fist
                stop_motor()
            elif (y <= 240):
                forward()
            elif (y >= 240):
                backward()

            if (x <= 150 and track_angle != 46): 
                for angle in range(track_angle, 45, -1):
                    left_rotate(angle)
                    track_angle = angle
                    # print(track_angle)
                    
            elif (x >= 530 and track_angle != 169):
                for angle in range(track_angle, 170):
                    right_rotate(angle)
                    track_angle = angle
                    # print(track_angle)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

except KeyboardInterrupt:
    stop_motor()

except Exception as e:
    print(e)
