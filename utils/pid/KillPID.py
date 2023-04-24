import os
import subprocess


def kill_pid(pid):
    """
    Kills the process with the specified PID.

    Parameters:
    pid (str): PID
    """

    if os.name == 'nt':
        subprocess.run(f'taskkill /pid {pid} /f >nul 2>&1', shell=True)
    
    else:
        subprocess.run(f'kill -SIGKILL {pid} > /dev/null 2>&1', shell=True)