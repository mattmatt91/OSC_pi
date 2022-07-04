

import time
import RPi.GPIO as GPIO

p1 = 21
p2 = 13
p3 = 22
p4 = 25
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(p1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    pressed = False
    while True:
        # button is pressed when pin is LOW
        if not GPIO.input(p1):
            if not pressed:
                print("Button pressed!")
                pressed = True
        # button not pressed (or released)
        else:
            pressed = False
        time.sleep(0.1)


import RPi.GPIO as GPIO
BUTTON_GPIO = 16
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while True:
        GPIO.wait_for_edge(BUTTON_GPIO, GPIO.FALLING)
        print("Button pressed!")