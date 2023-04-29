import subprocess

from utils.managers.Settings import SettingsManager


def check_ngrok():
    """
    Check if ngrok is installed on the system.

    Returns:
        bool: Returns true if it is installed
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    if subprocess.call(f'{settings["NGROK_COMMAND"]} version >nul 2>&1', shell=True) != 0:
        return False
    
    return True
