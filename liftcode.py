import RPi.GPIO as GPIO
import time

st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = False
sensor = [4, 17, 27, 22, 5, 6, 13, 19]
motor = [x, y]
enApin = z
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)

in1 = x
in2 = y
enA = GPIO.PWM(enApin, 100)
enA.start(0)
for i in sensor:
    GPIO.setup(i, GPIO.IN)
print("IR Sensor Ready.....")

currentFloor = 1
destination = 0


def forward():
    enA.ChangeDutyCycle(20)
    GPIO.output(in1, True)
    GPIO.output(in2, False)


def backward():
    enA.ChangeDutyCycle(20)
    GPIO.output(in1, False)
    GPIO.output(in2, True)


def stop():
    GPIO.output(in1, True)
    GPIO.output(in2, True)


try:
    while True:

        # internal elevator controller

        if GPIO.input(sensor[0]) == 0:
            destination = 1
            st1 = not st1
            print("1 Detected")
            if currentFloor < destination:
                print("==== Going down to 1st floor ====")
                forward()
            elif currentFloor == destination:
                print("Door Opened")
            while GPIO.input(sensor[0]) == 0:
                if GPIO.input(sensor[0]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[1]) == 0:
            destination = 2
            st2 = not st2
            print("2 Detected")
            if currentFloor < destination:
                print("==== Going down to 2nd floor ====")
                forward()
            elif currentFloor == destination:
                print("Door Opened")
            elif currentFloor > destination:
                print("==== Going up to 2nd floor ====")
                backward()
            while GPIO.input(sensor[1]) == 0:
                if GPIO.input(sensor[1]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[2]) == 0:
            destination = 3
            st3 = not st3
            print("3 Detected")
            if currentFloor == destination:
                print("Door Opened")
            elif currentFloor > destination:
                print("==== Going up to 3rd floor ====")
                backward()
            while GPIO.input(sensor[2]) == 0:
                if GPIO.input(sensor[2]) == 1:
                    break
            time.sleep(0.5)

        # external elevator controller

        elif GPIO.input(sensor[3]) == 0:
            st4 = not st4
            destination = 1
            print("Elevator called to 1st floor (UP)")
            if currentFloor < destination:
                forward()
            elif currentFloor == destination:
                print("Door Opened")
            while GPIO.input(sensor[3]) == 0:
                if GPIO.input(sensor[3]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[4]) == 0:
            st5 = not st5
            print("Elevator called to 2nd floor (UP)")
            if currentFloor < destination:
                print("==== Going down to 2nd floor ====")
                forward()
            elif currentFloor == destination:
                print("Door Opened")
            elif currentFloor > destination:
                print("==== Going up to 2nd floor ====")
                backward()
            while GPIO.input(sensor[4]) == 0:
                if GPIO.input(sensor[4]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[5]) == 0:
            st6 = not st6
            print("Elevator called to 2nd floor (DOWN)")
            if currentFloor < destination:
                print("==== Going down to 2nd floor ====")
                forward()
            elif currentFloor == destination:
                print("Door Opened")
            elif currentFloor > destination:
                print("==== Going up to 2nd floor ====")
                backward()
            while GPIO.input(sensor[5]) == 0:
                if GPIO.input(sensor[5]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[6]) == 0:
            st7 = not st7
            print("Object7 Detected")
            if currentFloor == destination:
                print("Door Opened")
            elif currentFloor > destination:
                print("==== Going up to 3rd floor ====")
                backward()
            while GPIO.input(sensor[6]) == 0:
                if GPIO.input(sensor[6]) == 1:
                    break
            time.sleep(0.5)

        elif GPIO.input(sensor[7]) == 0:
            st8 = not s
            if currentFloor < destination:
                currentFloor += 1
                print("Passed")
                time.sleep(1)
            elif currentFloor == destination:
                print("Door Opened")
                stop()
            elif currentFloor > destination:
                currentFloor -= 1
                print("Passed")
                time.sleep(1)
            while GPIO.input(sensor[7]) == 0:
                if GPIO.input(sensor[7]) == 1:
                    break
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()