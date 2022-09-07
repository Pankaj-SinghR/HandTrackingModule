import serial
import time
import cv2
import mediapipe as mp
import HandTrackingModule as htm

# for i in range(5):
#     print("Ping")
#     bluetooth.write(b"BOOP" + str.encode((str(i)))) #These need to be bytes not unicode, plus a number
#     input_data = bluetooth.readline()
#     print(input_data.decode())
#     time.sleep(0.1)
# bluetooth.close() #Otherwise the connection will remain open until a timeout
# print("Done")

try:
    print("Starting")
    port = '/dev/rfcomm0'
    bluetooth = serial.Serial(port, 9600)
    print("Connected")
    bluetooth.flushInput()

except Exception as e:
    print(e)

try:
    def forward():
        bluetooth.write(b''+str.encode((str(1)))) #BOOP1 mean move forward
        bluetooth.flush()

    def backward():
        bluetooth.write(b''+str.encode((str(2)))) #BOOP2 mean move backward
        bluetooth.flush()

    def stop_motor():
        bluetooth.write(b''+str.encode((str(0)))) #BOOP0 mean stop motor
        bluetooth.flush()

   
    def left_rotate():
        bluetooth.write(b''+str.encode((str(3)))) #BOOP3 mean move left
        bluetooth.flush()

    def right_rotate():
        bluetooth.write(b''+str.encode((str(4)))) #BOOP4 mean move right
        bluetooth.flush()

except Exception as e:
    print(e)

try:
    wCam, hCam = 640, 480

    cap = cv2.VideoCapture(0)
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
           
            if (lmlist[8][2] > lmlist[6][2]): # this will stop the motor if you make a fist
                stop_motor()

            elif (x > 200 and x < 580): #Middle grid
                if y <= 240:
                    forward()
                else:
                    backward()
           
            elif (x <= 200): #left grid
                left_rotate()
               
            elif (x >= 580): #right grid
                right_rotate()
           
        cv2.imshow("Image", img)
        cv2.waitKey(1)

except KeyboardInterrupt:
    stop_motor()
    bluetooth.close()

except Exception as e:
    print(e)
