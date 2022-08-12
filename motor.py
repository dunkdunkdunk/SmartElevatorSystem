import RPi.GPIO as GPIO
import time

motor = [x, y]
enApin = z
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)

in1 = x
in2 = y
enA = GPIO.PWM(enApin, 100)
enA.start(0)


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


while True:
    forward()
    time.sleep(1)
    backward()
    time.sleep(1)
    stop()
