from colorama import Fore, init
from src.decoration.mccolor import mcreplace

init()


def paint(text, end=None):
    """ 
    Apply Minecraft text formatting colors to the given text.

    This function replaces Minecraft formatting codes in the text with their respective
    colors using the `mcreplace` function. It then optionally appends an 'end' string 
    to the formatted text before printing it.

    Args:
        text (str): The input text to apply Minecraft formatting to.
        end (str): An optional string to append to the formatted text.
    """

    # Apply Minecraft text formatting codes to the input text.
    text = mcreplace(text)

    try:
        # Check if an 'end' string is provided and print accordingly.
        if end is not None:
            print(f'{text}{Fore.RESET}', end=end)

        else:
            print(f'{text}{Fore.RESET}')

    except UnicodeEncodeError:
        pass