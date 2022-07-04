from time import time, sleep
import RPi.GPIO as GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
for i in range(8,23):
     GPIO.setup(i, GPIO.IN)

data = []
_time = time()
for i in range(1000):
    msg = []
    for i in range(8,23):
        msg.append(GPIO.input(i))
    # print(msg)
print(time()-_time)
