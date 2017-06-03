# ------------------------
# Imports
# ------------------------

import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from datetime import datetime

# ------------------------
# Setup
# ------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ------------------------
# GPIO-pinnen
# ------------------------

pir = 20
led = 21
knop = 16
camera = PiCamera()

# ------------------------
# Test onderdelen
# ------------------------

GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(knop, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(led, GPIO.OUT)

try:
    while True:
        status = GPIO.input(pir)
        if status == 0:
            print("Niks gedetecteerd")
            GPIO.output(led, GPIO.LOW)
            time.sleep(1)
        elif status == 1:
            filename = "image-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
            print("Infrarood gedetecteerd, foto aan het nemen, even geduld")
            GPIO.output(led, GPIO.HIGH)
            time.sleep(5)
            camera.capture('/home/pi/Desktop/' + filename + '.jpg')
            print("Foto genomen")
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(led, GPIO.LOW)