import os


def check_folders(*folders):
    """ 
    Check if the following folders exist. 
    If they don't exist, create them.

    Args:
        *folders (list): Folder list,
    """

    for folder in folders:
        if isinstance(folder, str):
            if os.path.isdir(folder):
                pass
            else:
                os.mkdir(folder)
