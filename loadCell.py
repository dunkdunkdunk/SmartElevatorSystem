import RPi.GPIO as GPIO                # import GPIO
from hx711 import HX711                # import the class HX711

GPIO.setmode(GPIO.BCM)                 # set GPIO pin mode to BCM numbering
hx = HX711(dout_pin=x, pd_sck_pin=y)
while True:
    print(hx)