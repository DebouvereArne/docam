# ------------------------
# Imports
# ------------------------

import pygame                           # Afspelen audio via bluetooth-speaker
import RPi.GPIO as GPIO                 # GPIO
import time                             # Time
from picamera import PiCamera           # Pi camera-module
from datetime import datetime           # Datetime
from subprocess import call

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
knop = 16                               # Deurbel
#buzzer

# ------------------------
# Andere
# ------------------------

camera = PiCamera()                     # Camera-instantie
aangebeld = False                       # Controleren of er aangebeld werd of niet
motion_detected = False                 # Beweging waargenomen of niet
motion_sensor = True
default_width = 1280                    # Default width
default_height = 720                    # Default height
brightness = 60                         # Default brightness
video_duration = 20                     # Duur van de video in seconden
ringtone_name = "clarinet"              # Bestandsaam van de ringtone
framerate = 60                          # Default framerate van video's

# ------------------------
# Test onderdelen
# ------------------------

GPIO.setup(pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(knop, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)

def cameraSettings():
    camera.resolution = (default_width, default_height)
    camera.brightness = brightness

def cameraImageSettings():
    pass

def cameraVideoSettings():
    camera.framerate = framerate

def my_callback(channel):
    if (GPIO.input(knop)):
        aangebeld = True
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Music/Ringtones/" + ringtone_name + ".mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

GPIO.add_event_detect(knop, GPIO.RISING, callback=my_callback, bouncetime=200)

def take_picture():
    statusSensor = GPIO.input(pir)
    if statusSensor == 0:
        GPIO.output(led, GPIO.LOW)
    elif statusSensor == 1:
        motion_detected = True
        filename = "image-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
        print("Infrarood gedetecteerd, foto aan het nemen, even geduld")
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        cameraSettings()
        camera.start_preview()
        time.sleep(2)                                                           # Scherpstellen van de camera
        camera.capture('/home/pi/Pictures/' + filename + '.jpg')
        print("Foto genomen")
        time.sleep(30)
        motion_detected = False

def record_video():
    statusSensor = GPIO.input(pir)
    if statusSensor == 0:
        GPIO.output(led, GPIO.LOW)
    elif statusSensor == 1:
        filename = "video-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
        print("Infrarood gedetecteerd, video aan het opnemen, even geduld")
        motion_detected = True
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(led, GPIO.LOW)
        cameraSettings()
        cameraVideoSettings()
        camera.start_recording('/home/pi/Videos/' + filename + '.h264')
        time.sleep(video_duration)
        camera.stop_recording()
        cmd = "MP4Box -add /home/pi/Videos/" + filename + ".h264:fps=" + str(framerate) + "-new /home/pi/Videos/" + filename + ".mp4"
        call([cmd], shell=True)
        print("Video opgenomen")
        time.sleep(3)
        motion_detected = False

try:
    while motion_sensor == True:
        #take_picture()
        record_video()

except KeyboardInterrupt:
    GPIO.output(led, GPIO.LOW)