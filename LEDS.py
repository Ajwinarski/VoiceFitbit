import RPi.GPIO as GPIO
import time

from pixels import pixels

GPIO.setmode(GPIO.BCM)

# NOTE: BELOW, THE PINS ARE DEFINED AS !!! OUT !!!
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
pixels.off()

BothPin56 = ''

while True:
    pin5_state = GPIO.input(5)
    pin6_state = GPIO.input(6)
    print('Pin 5 = ' + str(pin5_state) + ', Pin 6 = ' + str(pin6_state) + BothPin56
    if pin5_state == 1:
    pin6_state = GPIO.input(6)
    print('Pin 5 = ' + str(pin5_state) + ', Pin 6 = ' + str(pin6_state) + BothPin56
    if pin5_state == 1:
       pixels.think()
       time.sleep(0.6)
       BothPin56 = ''
    if pin6_state == 1:
       pixels.speak()
       time.sleep(0.6)
       BothPin56 = ''
    if pin5_state == 0 and pin6_state == 0:
       pixels.off()
       time.sleep(0.6)
       BothPin56 = ', LEDS OFF'

pixels.off()
GPIO.cleanup()
