import pygame
pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Music/Scooter - You.mp3")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue