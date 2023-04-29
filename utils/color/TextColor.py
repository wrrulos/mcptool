from colorama import Fore, init
from utils.mccolor import mcreplace

init()


def paint(text, end=None):
    """ 
    Replace Minecraft characters with their 
    respective colors.
    
    Parameters:
        text (str): Text
        end (str): Decide if the text should end with something specific.
    """

    text = mcreplace(text)

    if end is not None:
        print(f'{text}{Fore.RESET}', end=end)

    else:
        print(f'{text}{Fore.RESET}')
