#!/usr/bin/python3

from colorama import Fore, init

init()


def paint(text, end=None):
    """ 
    Replace the texts with their colors 
    
    :param text: Text
    :param end: Decide if the text should end with something specific.
    """

    color_texts = ['[red]', '[lred]', '[black]', '[lblack]', '[white]',
                   '[lwhite]', '[green]', '[lgreen]', '[cyan]', '[lcyan]',
                   '[magenta]', '[lmagenta]', '[yellow]', '[lyellow]', '[blue]', 
                   '[lblue]']

    colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.BLACK, Fore.LIGHTBLACK_EX, Fore.WHITE, Fore.LIGHTWHITE_EX, Fore.GREEN, 
              Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.YELLOW, 
              Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTBLUE_EX]

    for num, color in enumerate(color_texts):
        text = text.replace(color, colors[int(num)])

    if end is not None:
        print(f'{text}{Fore.RESET}', end=end)

    else:
        print(f'{text}{Fore.RESET}')

    return
