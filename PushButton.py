# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Jarbas Horst wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# This code shows how to interact with a push button and Raspberry PI.
# ----------------------------------------------------------------------------

# Imports GPIO and time library.
import RPi.GPIO as GPIO
import time
# BCM: Describes numbers of GPIO pins.
GPIO.setmode(GPIO.BCM)
# GPIO.PUD_UP: Defines button event which will be handled.
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if (GPIO.input(23) == 0):
            print('It works!')
            time.sleep(0.2)
except Exception as e:
    GPIO.cleanup()
    print('\033[91m')
    print(e)
    print('\033[0m')
