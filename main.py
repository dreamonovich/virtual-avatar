import numpy as np
import sounddevice as sd
from collections import deque
import pygame
import sys
import threading

SILENCE_THRESHOLD = 15
MAX_VOLUME = 60
VOLUME_HISTORY_SIZE = 10

volume_history = deque(maxlen=VOLUME_HISTORY_SIZE)

pygame.init()

sprite1 = pygame.image.load("sprites/1.png")
sprite2 = pygame.image.load("sprites/2.png")
sprite3 = pygame.image.load("sprites/3.png")
sprite4 = pygame.image.load("sprites/4.png")
sprite5 = pygame.image.load("sprites/5.png")
sprite6 = pygame.image.load("sprites/6.png")

screen = pygame.display.set_mode(sprite1.get_size())


def update_sprite(volume):
    sprites = [sprite1, sprite2, sprite3, sprite4, sprite5, sprite6]

    if volume > MAX_VOLUME:
        volume = MAX_VOLUME
    elif volume < SILENCE_THRESHOLD:
        volume = 0

    file_index = round(volume * (len(sprites)-1) / MAX_VOLUME)

    screen.blit(sprites[file_index], (0, 0))


def stream_callback(indata, frames, time, status):
    global volume_history

    volume = np.sqrt(np.mean(indata**2))
    volume_history.append(volume)

    average_volume = np.mean(volume_history)

    update_sprite(int(average_volume * 1000))



def start_audio_stream():
    stream = sd.InputStream(callback=stream_callback)
    with stream:
        while True:
            sd.sleep(10)


audio_thread = threading.Thread(target=start_audio_stream)
audio_thread.start()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
