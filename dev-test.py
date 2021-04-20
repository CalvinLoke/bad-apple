import pygame
from pygame import mixer

path_to_file = 'bad-apple-audio.mp3'

pygame.init()
mixer.pre_init(44100, -16, 2, 2048)
mixer.init()
mixer.music.load(path_to_file)
mixer.music.play()

while mixer.music.get_busy():
    pygame.time.Clock().tick(10)


