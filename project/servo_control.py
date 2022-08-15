from multiprocessing.context import SpawnProcess
from pyfirmata import Arduino, SERVO, INPUT, OUTPUT, PWM
from time import sleep

try:
    Arduino_port = '/dev/ttyUSB0'
    pin = 10
    board = Arduino(Arduino_port)

    #set mode of pin
    board.digital[pin].mode = SERVO
    board.digital[pin].write(115)
    sleep(2)
    # print(SERVO)

    In1 = 7
    In2 = 8

    board.digital[In1].mode = OUTPUT
    board.digital[In2].mode = OUTPUT


    def direction1():
        board.digital[In1].write(1)
        board.digital[In2].write(0)

    def direction2():
        board.digital[In1].write(0)
        board.digital[In2].write(1)

    direction1()
    direction2()

    def rotateServo(pin, angle):
        board.digital[pin].write(angle)
        print(angle)
        sleep(1)

    while True:
        for i in range(0, 180):
            rotateServo(pin, i)
            # direction1()

        for j in range(180, 0, -1):
            rotateServo(pin, j)
            # direction2()

except KeyboardInterrupt:
    board.digital[In1].write(0)
    board.digital[In2].write(0)

except Exception as e:
    print(e)
