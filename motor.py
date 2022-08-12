import RPi.GPIO as GPIO
import time

st1 = st2 = st3 = st4 = st5 = st6 = st7 = st8 = False

sensor = [4, 17, 27, 22, 5, 6, 13, 19]
GPIO.setmode(GPIO.BOARD)

for i in sensor:
    GPIO.setup(i, GPIO.IN)
print("IR Sensor Ready.....")
try:
    while True:
        if GPIO.input(sensor[0]) == 0:
            st1 = not st1
            print("Object1 Detected")
            while GPIO.input(sensor[0]) == 0:
                if GPIO.input(sensor[0]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[1]) == 0:
            st2 = not st2
            print("Object2 Detected")
            while GPIO.input(sensor[1]) == 0:
                if GPIO.input(sensor[1]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[2]) == 0:
            st3 = not st3
            print("Object3 Detected")
            while GPIO.input(sensor[2]) == 0:
                if GPIO.input(sensor[2]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[3]) == 0:
            st4 = not st4
            print("Object4 Detected")
            while GPIO.input(sensor[3]) == 0:
                if GPIO.input(sensor[3]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[4]) == 0:
            st5 = not st5
            print("Object5 Detected")
            while GPIO.input(sensor[4]) == 0:
                if GPIO.input(sensor[4]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[5]) == 0:
            st6 = not st6
            print("Object6 Detected")
            while GPIO.input(sensor[5]) == 0:
                if GPIO.input(sensor[5]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[6]) == 0:
            st7 = not st7
            print("Object7 Detected")
            while GPIO.input(sensor[6]) == 0:
                if GPIO.input(sensor[6]) == 1:
                    break
            time.sleep(0.5)
        elif GPIO.input(sensor[7]) == 0:
            st8 = not s
            print("Object8 Detected")
            while GPIO.input(sensor[7]) == 0:
                if GPIO.input(sensor[7]) == 1:
                    break
            time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
