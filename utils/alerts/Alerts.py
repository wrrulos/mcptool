import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


def alert(name):
    """
    Play an audio to use as a notification.

    Parameters:
        name (str): Sound name
    """

    try:
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(f'utils/alerts/sounds/{name}.mp3')
        pygame.mixer.Sound.play(sound)

    except pygame.error:
        return
