import subprocess


def check_masscan():
    """
    Check if nmap is installed on the system.

    Returns:
        bool: Returns true if it is installed
    """

    if subprocess.call(f'masscan --version >nul 2>&1', shell=True) != 0:
        return False

    return True