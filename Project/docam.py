# ------------------------
# Imports
# ------------------------

import pygame                           # Afspelen audio via bluetooth-speaker
import RPi.GPIO as GPIO                 # GPIO
import time                             # Time
from picamera import PiCamera           # Pi camera-module
from datetime import datetime           # Datetime

# ------------------------
# Setup
# ------------------------

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)                 # Negeren van GPIO-waarschuwingen

# ------------------------
# GPIO-pinnen
# ------------------------

pir = 20                                # Passieve infraroodsensor
led = 21                                # LED (visuel aantonen dat de knop/sensor iets heeft opgenomen)
#led2? mogelijke tweede LED voor belichting 's nachts
knop = 16                               # Deurbel

# ------------------------
# Andere
# ------------------------

camera = PiCamera()                     # Camera-instantie
aangebeld = False                       # Controleren of er aangebeld werd of niet

# ------------------------
# Test onderdelen
# ------------------------

GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(knop, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

try:
    def my_callback(args):
        aangebeld = True
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Music/Scooter - You.mp3")  # Testmuziek (later ringtones)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:  # Zorgt ervoor dat de muziek blijft spelen tot het einde
            continue
    GPIO.add_event_detect(knop, GPIO.RISING, callback=my_callback, bouncetime=200)

    while True:
        # ----------------
        # Infraroodsensor
        # ----------------

        statusSensor = GPIO.input(pir)                                  # Controleren of er infraroodbeweging is
        if statusSensor == 0:                                           # Wordt uitgevoerd mits er geen infraroodbeweging wordt opgenomen
            print("Niks gedetecteerd")
            GPIO.output(led, GPIO.LOW)
            time.sleep(1)
        elif statusSensor == 1:
            filename = "image-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))     # Naamformaat voor opslag van de afbeelding
            print("Infrarood gedetecteerd, foto aan het nemen, even geduld")
            GPIO.output(led, GPIO.HIGH)
            time.sleep(5)                                                               # Scherpstellen van de camera
            camera.capture('/home/pi/Desktop/' + filename + '.jpg')                     # Nemen van de foto
            print("Foto genomen")
            time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(led, GPIO.LOW)