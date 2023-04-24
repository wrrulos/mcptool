import os


def check_folders(*folders):
    """ 
    Check if the following folders exist. 
    If they don't exist, create them.

    Parameters:
    *folders (list): Folder list,
    """

    for folder in folders:
        if os.path.isdir(folder):
            pass

        else:
            os.mkdir(folder)
