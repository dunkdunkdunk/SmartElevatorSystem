import RPi.GPIO as GPIO
import time

motor = [20, 21]
enApin = 16
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)
GPIO.setup(enApin,GPIO.OUT)
in1 = 20
in2 = 21
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
