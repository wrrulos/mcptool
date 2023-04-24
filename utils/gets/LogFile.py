from datetime import datetime
from utils.checks.Folder import check_folders


def create_file(command):
    """
    Create the file that will be used to store data

    Parameters:
    command (str): Command name

    Returns:
    str: File
    """

    date = datetime.now()
    t = f'{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}'

    check_folders('logs', f'logs/{command}')
    file = f'logs/{command}/{command.capitalize()}_{t}.txt'
    return file