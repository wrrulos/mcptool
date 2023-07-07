import subprocess
import os

from utils.checks.check_termux import check_termux


def play_sound(sound_name):
    """
    Play an audio to use as a notification.

    Parameters:
        sound_name (str): Sound name
    """

    if not check_termux():
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
        import pygame

        try:
            pygame.init()
            pygame.mixer.init()
            sound = pygame.mixer.Sound(f'utils/sounds/sounds/{sound_name}.mp3')
            pygame.mixer.Sound.play(sound)

        except pygame.error:
            return
        
    else:
        subprocess.Popen(f'play utils/sounds/sounds/{sound_name}.mp3 >nul 2>&1', shell=True)
