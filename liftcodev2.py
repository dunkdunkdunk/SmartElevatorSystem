#import dependencies
import RPi.GPIO as GPIO
import time
from datetime import datetime
import multiprocessing
import pandas as pd
import requests

#forward motor function
def forward(speed, in1, in2, enA):
    enA.ChangeDutyCycle(speed)
    GPIO.output(in1, True)
    GPIO.output(in2, False)

#backward motor function
def backward(speed, in1, in2, enA):
    enA.ChangeDutyCycle(5)
    GPIO.output(in1, False)
    GPIO.output(in2, True)

#stop motor function
def stop(in1, in2,enA):
    enA.ChangeDutyCycle(10)
    GPIO.output(in1, True)
    GPIO.output(in2, False)
    

def openliftdoor(in3,in4,in5,in6) :
    GPIO.output(in3,True)
    GPIO.output(in4,False)
    GPIO.output(in5, False)
    GPIO.output(in6, True)

def closeliftdoor(in3,in4,in5,in6):
    GPIO.output(in3, False)
    GPIO.output(in4, True)
    GPIO.output(in5,True)
    GPIO.output(in6,False)

def stopliftdoor(in3,in4,in5,in6):
    GPIO.output(in3,False)
    GPIO.output(in4,False)
    GPIO.output(in5,False)
    GPIO.output(in6,False)

def liftcode(data1):
    #define each state for each IR sensor
    st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = st9 = False
    #IR sensor GPIO PIN
    sensor = [4, 17, 27, 22, 5, 6, 13, 19, 26]
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

    try:
        while True:

            # internal elevator controller
            if GPIO.input(sensor[0]) == 0:
                destination = 1
                st1 = not st1
                print("==== 1 Detected ====")
                if currentFloor > destination:
                    print("==== Going down to 1st floor ====")
                    backward(speed,in1,in2,enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    backward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    if doorIsOpened :
                        print("==== Arrived ====")
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                        backward(speed,in1,in2,enA)
                        time.sleep(0.7)
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
                    forward(speed, in1, in2, enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    if doorIsOpened :
                        print("==== Arrived ====")
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed,in1,in2,enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    backward(speed, in1, in2, enA)
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
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                        backward(speed,in1,in2,enA)
                        time.sleep(1.2)
                elif currentFloor < destination:
                    print("==== Going up to 3rd floor ====")
                    forward(speed, in1, in2, enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    forward(speed, in1, in2, enA)
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
                    backward(speed,in1,in2,enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    backward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    if doorIsOpened :
                        print("==== Arrived ====")
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
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
                    forward(speed, in1, in2, enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    if doorIsOpened :
                        print("==== Arrived ====")
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed,in1,in2,enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    backward(speed, in1, in2, enA)
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
                    forward(speed, in1, in2, enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    if doorIsOpened :
                        print("==== Arrived ====")
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed,in1,in2,enA)
                    time.sleep(0.2)
                    stop(in1,in2,enA)
                    backward(speed, in1, in2, enA)
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
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                        backward(speed,in1,in2,enA)
                        time.sleep(1.2)
                elif currentFloor < destination:
                    print("==== Going up to 3rd floor ====")
                    forward(speed, in1, in2, enA)
                while GPIO.input(sensor[6]) == 0:
                    if GPIO.input(sensor[6]) == 1:
                        break
                time.sleep(0.5)

            elif GPIO.input(sensor[7]) == 0:
                if currentFloor == 1 and destination == 0 :
                    destination += 1
                    forward(speed, in1, in2, enA)
                    time.sleep(0.9)
                    stop(in1, in2,enA)
                st8 = not st8
                if currentFloor < destination:
                    time.sleep(1)
                    currentFloor += 1
                    print("==== Current Floor",currentFloor,"====")
                    data1.send(currentFloor)
                    print("==== Passed ====")
                    if currentFloor == destination:
                        data1.send(currentFloor)
                        if doorIsOpened :
                            print("==== Arrived ====")
                            stop(in1, in2,enA)
                            time.sleep(1)
                            openliftdoor(in3,in4,in5,in6)
                            time.sleep(1.5)
                            stopliftdoor(in3,in4,in5,in6)
                            time.sleep(5)
                            closeliftdoor(in3,in4,in5,in6)
                            time.sleep(1.5)
                            stopliftdoor(in3,in4,in5,in6)
                            print("==== Door Opened ====")
                    time.sleep(2)
                elif currentFloor == destination:
                    data1.send(currentFloor)
                    print("=== Door Opened ===")
                    if doorIsOpened :
                        print("==== Arrived ====")
                        stop(in1, in2,enA)
                        time.sleep(1)
                        openliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        time.sleep(5)
                        closeliftdoor(in3,in4,in5,in6)
                        time.sleep(1.5)
                        stopliftdoor(in3,in4,in5,in6)
                        print("==== Door Opened ====")
                elif currentFloor > destination:
                    forward(speed, in1, in2, enA)
                    time.sleep(0.7)
                    stop(in1, in2,enA)
                    currentFloor -= 1
                    print("==== Current Floor",currentFloor,"====")
                    data1.send(currentFloor)
                    print("==== Passed ====")
                    if currentFloor == destination:
                        data1.send(currentFloor)
                        if doorIsOpened :
                            print("==== Arrived ====")
                            stop(in1, in2,enA)
                            time.sleep(1)
                            openliftdoor(in3,in4,in5,in6)
                            time.sleep(1.5)
                            stopliftdoor(in3,in4,in5,in6)
                            time.sleep(5)
                            closeliftdoor(in3,in4,in5,in6)
                            time.sleep(1.5)
                            stopliftdoor(in3,in4,in5,in6)
                            print("==== Door Opened ====")
                    time.sleep(2)
                while GPIO.input(sensor[7]) == 0:
                    if GPIO.input(sensor[7]) == 1:
                        break
                time.sleep(0.5)

    except KeyboardInterrupt:
        if currentFloor != 1 :
            backward(speed,in1,in2,enA)
            
        GPIO.cleanup()

def sendData(data):

    REST_API_URL = 'https://api.powerbi.com/beta/a6901d0c-e6ce-4ac7-93d5-6d406d25285f/datasets/96fa3ba6-b8a0-43cf-8855-8043505c3019/rows?key=NrhanNwnoNtsfpARoY1bbg2nllJUQq8Ako%2FXGPnJlIy9Zt43EFlrqC9wm%2BmyVqpWz5wyd%2F87AvAzYni3HNyD1Q%3D%3D'

    # while True:
    data_raw = []
    for i in range(1):
        row = [data,datetime.today().strftime("%Y-%m-%d"),datetime.now().isoformat()]
        data_raw.append(row)
        print("Raw data - ", data_raw)

    # set the header record
    HEADER = ["floor","time","date"]

    data_df = pd.DataFrame(data_raw, columns=HEADER)
    data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
    print("JSON dataset", data_json)

    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_json)

    print("Data posted in Power BI API")


if __name__ == '__main__':
    data1, data2 = multiprocessing.Pipe()

    elevatorProcess = multiprocessing.Process(target=liftcode, args=(data2,))
    elevatorProcess.start()
    while True:
        dataVal = data1.recv()

        pbiProcess = multiprocessing.Process(target=sendData, args=(dataVal,))
        pbiProcess.start()
        pbiProcess.join()
