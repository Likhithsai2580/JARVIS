import os
import pygame
from functools import lru_cache

# Cache the 'mid' function
@lru_cache(maxsize=128)  # Adjust maxsize according to your memory constraints
def mid(text):
    command = f'edge-tts --voice "en-CA-LiamNeural" --pitch=+9Hz --rate=+22% --text "{text}" --write-media "data.mp3"'
    os.system(command)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("data.mp3")
    try:
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    return "data.mp3"
