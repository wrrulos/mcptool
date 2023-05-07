import os
import platform
import subprocess
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

script_dir = os.path.dirname(os.path.abspath(__file__))

def is_termux_api_installed():
    try:
        subprocess.check_output(['termux-media-player'], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def alert(name):
    """
    Play an audio to use as a notification.

    Parameters:
        name (str): Sound name
    """
    # detect if MCPTool is running on Termux
    if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
        if is_termux_api_installed():
            sound_file_path = os.path.join(script_dir, f'sounds/{name}.mp3')
            subprocess.run(['termux-media-player', 'play', sound_file_path], check=True)
        else:
            raise Exception('Termux environment detected but couldn\'t find Termux:API. Please install it.')
    else:
        import pygame
        try:
            pygame.init()
            pygame.mixer.init()
            sound = pygame.mixer.Sound(f'utils/alerts/sounds/{name}.mp3')
            pygame.mixer.Sound.play(sound)

        except pygame.error:
            return
