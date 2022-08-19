import RPi.GPIO as GPIO
import time
st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = st9 = False
#IR sensor GPIO PIN
sensor = [4, 17,27, 22, 5, 6, 13, 19, 26]
#motor & enA GPIO PIN 
in1 = 20
in2 = 21
in3 = 8
in4 = 25
in5 = 1
in6 = 7
motor = [in1,in2,in3,in4,in5,in6]
enApin = 16
#speed for motor
speed = 100
#setmode as BCM
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)

GPIO.setup(enApin,GPIO.OUT)
enA = GPIO.PWM(enApin, 50)
enA.start(0)
GPIO.output(in3,True)
GPIO.output(in4,True)
for i in sensor:
    GPIO.setup(i, GPIO.IN)
print("IR Sensor Ready.....")
doorIsOpened = True
currentFloor = 1
destination = 0

while True:
    # print(GPIO.input(sensor[4]) )
    # internal elevator controller

    if GPIO.input(sensor[0]) == 0:
        destination = 1
        st1 = not st1
        print("==== 1 Detected ====")
        if currentFloor > destination:
            print("==== Going down to 1st floor ====")
            
        elif currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        while GPIO.input(sensor[0]) == 0:
            if GPIO.input(sensor[0]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[1]) == 0:
        destination = 2
        st2 = not st2
        print("==== 2 Detected ====")
        if currentFloor < destination:
            print("==== Going up to 2nd floor ====")
        elif currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        elif currentFloor > destination:
            print("==== Going down to 2nd floor ====")
            
        while GPIO.input(sensor[1]) == 0:
            if GPIO.input(sensor[1]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[2]) == 0:
        destination = 3
        st3 = not st3
        print("==== 3 Detected ====")
        if currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        elif currentFloor < destination:
            print("==== Going up to 3rd floor ====")
        while GPIO.input(sensor[2]) == 0:
            if GPIO.input(sensor[2]) == 1:
                break
        time.sleep(0.5)

    # external elevator controller

    elif GPIO.input(sensor[3]) == 0:
        st4 = not st4
        destination = 1
        print("==== Elevator called to 1st floor (UP) ====")
        if currentFloor > destination:
            print("1 UP")
        elif currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        while GPIO.input(sensor[3]) == 0:
            if GPIO.input(sensor[3]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[4]) == 0:
        st5 = not st5
        destination = 2
        print("==== Elevator called to 2nd floor (UP) ====")
        if currentFloor < destination:
            print("==== Going up to 2nd floor ====")
        elif currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        elif currentFloor > destination:
            print("==== Going down to 2nd floor ====")
            
        while GPIO.input(sensor[4]) == 0:
            if GPIO.input(sensor[4]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[5]) == 0:
        st6 = not st6
        destination = 2
        print("==== Elevator called to 2nd floor (DOWN) ====")
        if currentFloor < destination:
            print("==== Going up to 2nd floor ====")
        elif currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        elif currentFloor > destination:
            print("==== Going down to 2nd floor ====")
            
        while GPIO.input(sensor[5]) == 0:
            if GPIO.input(sensor[5]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[6]) == 0:
        st7 = not st7
        destination = 3
        print("==== Elevator called to 3rd floor (DOWN) ====")
        if currentFloor == destination:
            if doorIsOpened :
                print("==== Arrived ====")
                print("==== Door Opened ====")
        elif currentFloor < destination:
            print("==== Going up to 3rd floor ====")
        while GPIO.input(sensor[6]) == 0:
            if GPIO.input(sensor[6]) == 1:
                break
        time.sleep(0.5)

    elif GPIO.input(sensor[7]) == 0:
        st8 = not st8
        print(7)