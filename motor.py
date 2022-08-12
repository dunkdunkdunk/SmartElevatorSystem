import RPi.GPIO as GPIO
import time

motor = [x, y]
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)

in1 = x
in2 = y


def forward():
    GPIO.output(in1, True)
    GPIO.output(in2, False)


def backward():
    GPIO.output(in1, False)
    GPIO.output(in2, True)


def stop():
    GPIO.output(in1, True)
    GPIO.output(in2, True)


while True:
    forward()
    time.sleep(1)
    backward()
    time.sleep(1)
    stop()
