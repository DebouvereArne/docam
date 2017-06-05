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
resizeImage = False
default_width = 1280
default_height = 720
custom_width = 1280
custom_height = 720
brightness = 80
video_duration = 30
ringtone_name = "clarinet"

# ------------------------
# Test onderdelen
# ------------------------

GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(knop, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

def customResolution(width, height):
    custom_width = width
    custom_height = height

def cameraSettings():
    camera.resolution = (default_width, default_height)
    camera.brightness = brightness

def my_callback(channel):
    if (GPIO.input(knop)):
        aangebeld = True
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Music/Ringtones/" + ringtone_name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

GPIO.add_event_detect(knop, GPIO.RISING, callback=my_callback, bouncetime=200)

def takePicture():
    statusSensor = GPIO.input(pir)
    if statusSensor == 0:
        GPIO.output(led, GPIO.LOW)
    elif statusSensor == 1:
        filename = "image-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
        print("Infrarood gedetecteerd, foto aan het nemen, even geduld")
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        cameraSettings()
        camera.start_preview()
        time.sleep(2)       # Scherpstellen van de camera
        if (default_width != custom_width or default_height != custom_height):
            camera.capture('/home/pi/Pictures/' + filename + '.jpg', resize=(custom_width, custom_height))
        else:
            camera.capture('/home/pi/Pictures/' + filename + '.jpg')
        print("Foto genomen")
        time.sleep(30)

def recordVideo():
    statusSensor = GPIO.input(pir)  # Controleren of er infraroodbeweging is
    if statusSensor == 0:  # Wordt uitgevoerd mits er geen infraroodbeweging wordt opgenomen
        GPIO.output(led, GPIO.LOW)
    elif statusSensor == 1:
        filename = "video-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
        print("Infrarood gedetecteerd, video aan het opnemen, even geduld")
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        cameraSettings()
        camera.start_recording('/home/pi/Videos/' + filename + '.h264')
        time.sleep(video_duration)
        camera.stop_recording()
        print("Video opgenomen")
        time.sleep(3)

try:
    while True:
        takePicture()
        #recordVideo()

except KeyboardInterrupt:
    GPIO.output(led, GPIO.LOW)