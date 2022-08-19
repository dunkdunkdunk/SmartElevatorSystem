import time
import RPi.GPIO as GPIO
in3 = 8
in4 = 25
in5 = 1
in6 = 7
motor = [in3,in4,in5,in6]
#setmode as BCM
GPIO.setmode(GPIO.BCM)

for i in motor:
    GPIO.setup(i, GPIO.OUT)
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

while True:
    openliftdoor(in3,in4,in5,in6)
    time.sleep(2)
    stopliftdoor(in3,in4,in5,in6)
    time.sleep(1)
    closeliftdoor(in3,in4,in5,in6)
    time.sleep(2)