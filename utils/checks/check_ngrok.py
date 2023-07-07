import subprocess

from utils.managers.config_manager import config_manager


def check_ngrok():
    """
    Check if ngrok is installed on the system.

    Returns:
        bool: Returns true if it is installed
    """

    if subprocess.call(f'{config_manager.config["commands"]["ngrok"]} version >nul 2>&1', shell=True) != 0:
        return False
    
    return True
