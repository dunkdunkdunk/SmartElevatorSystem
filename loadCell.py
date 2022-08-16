import RPi.GPIO as GPIO                # import GPIO
from hx711 import HX711                # import the class HX711

GPIO.setmode(GPIO.BCM)
x = 25
y = 26
GPIO.setup(x,GPIO.IN)
GPIO.setup(y,GPIO.IN)

hx = HX711(dout_pin=x, pd_sck_pin=y)
hx.set_reading_format("MSB","MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()
print("Tare Done!")
while True :
    try :
        val = hx.get_weight(x)
        print(round(val),"Grams")

        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
    except(KeyboardInterrupt,SystemExit):
        GPIO.cleanup()
