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
    enA.ChangeDutyCycle(speed)
    GPIO.output(in1, False)
    GPIO.output(in2, True)

#stop motor function
def stop(in1, in2):
    GPIO.output(in1, True)
    GPIO.output(in2, True)

def liftcode(data1):
    #define each state for each IR sensor
    st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = False
    #IR sensor GPIO PIN
    sensor = [4, 17, 27, 22, 5, 6, 13, 19]
    #motor & enA GPIO PIN 
    in1 = 20
    in2 = 21
    motor = [in1,in2]
    enApin = 16
    #speed for motor
    speed = 30
    #setmode as BCM
    GPIO.setmode(GPIO.BCM)
    for i in motor:
        GPIO.setup(i, GPIO.OUT)
    GPIO.setup(enApin,GPIO.OUT)
    enA = GPIO.PWM(enApin, 50)
    enA.start(0)
    for i in sensor:
        GPIO.setup(i, GPIO.IN)
    print("IR Sensor Ready.....")

    currentFloor = 1
    destination = 0

    try:
        while True:

            # internal elevator controller

            if GPIO.input(sensor[0]) == 0:
                destination = 1
                st1 = not st1
                print("1 Detected")
                if currentFloor > destination:
                    print("==== Going down to 1st floor ====")
                    backward(speed, in1, in2, enA)
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
                    print("==== Going up to 2nd floor ====")
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    print("Door Opened")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed, in1, in2, enA)
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
                elif currentFloor < destination:
                    print("==== Going up to 3rd floor ====")
                    forward(speed, in1, in2, enA)
                while GPIO.input(sensor[2]) == 0:
                    if GPIO.input(sensor[2]) == 1:
                        break
                time.sleep(0.5)

            # external elevator controller

            elif GPIO.input(sensor[3]) == 0:
                st4 = not st4
                destination = 1
                print("Elevator called to 1st floor (UP)")
                if currentFloor > destination:
                    backward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    print("Door Opened")
                while GPIO.input(sensor[3]) == 0:
                    if GPIO.input(sensor[3]) == 1:
                        break
                time.sleep(0.5)

            elif GPIO.input(sensor[4]) == 0:
                st5 = not st5
                destination = 2
                print("Elevator called to 2nd floor (UP)")
                if currentFloor < destination:
                    print("==== Going up to 2nd floor ====")
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    print("Door Opened")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed, in1, in2, enA)
                while GPIO.input(sensor[4]) == 0:
                    if GPIO.input(sensor[4]) == 1:
                        break
                time.sleep(0.5)

            elif GPIO.input(sensor[5]) == 0:
                st6 = not st6
                destination = 2
                print("Elevator called to 2nd floor (DOWN)")
                if currentFloor < destination:
                    print("==== Going up to 2nd floor ====")
                    forward(speed, in1, in2, enA)
                elif currentFloor == destination:
                    print("Door Opened")
                elif currentFloor > destination:
                    print("==== Going down to 2nd floor ====")
                    backward(speed, in1, in2, enA)
                while GPIO.input(sensor[5]) == 0:
                    if GPIO.input(sensor[5]) == 1:
                        break
                time.sleep(0.5)

            elif GPIO.input(sensor[6]) == 0:
                st7 = not st7
                destination = 3
                print("Elevator called to 3rd floor (DOWN)")
                if currentFloor == destination:
                    print("Door Opened")
                elif currentFloor < destination:
                    print("==== Going up to 3rd floor ====")
                    forward(speed, in1, in2, enA)
                while GPIO.input(sensor[6]) == 0:
                    if GPIO.input(sensor[6]) == 1:
                        break
                time.sleep(0.5)

            elif GPIO.input(sensor[7]) == 0:
                st8 = not st8
                if currentFloor < destination:
                    currentFloor += 1
                    print("Current Floor",currentFloor)
                    data1.send(currentFloor)
                    print("Passed")
                    if currentFloor == destination:
                        data1.send(currentFloor)
                        print("Door Opened")
                        stop(in1, in2)
                    time.sleep(1)
                elif currentFloor == destination:
                    data1.send(currentFloor)
                    print("Door Opened")
                    stop(in1, in2)
                elif currentFloor > destination:
                    currentFloor -= 1
                    print("Current Floor",currentFloor)
                    data1.send(currentFloor)
                    print("Passed")
                    if currentFloor == destination:
                        data1.send(currentFloor)
                        print("Door Opened")
                        stop(in1, in2)
                    time.sleep(1)
                while GPIO.input(sensor[7]) == 0:
                    if GPIO.input(sensor[7]) == 1:
                        break
                time.sleep(0.5)

    except KeyboardInterrupt:
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