#!/usr/bin/python3

from colorama import Fore, init

init()


def remove_colors(text):
    """ 
    Remove colored characters 
    
    :param text: Text
    :return: New Text
    """

    colored_characters = ['§0', '§1', '§2', '§3', '§4', '§5', 
                          '§6', '§7', '§8', '§9', '§a', '§b', 
                          '§c', '§d', '§e', '§f', '§k', '§l', 
                          '§m', '§n', '§o', '§r', '§A', '§B', 
                          '§C', '§D', '§E', '§F', '§K', '§L', 
                          '§M', '§N', '§O', '§R']

    for character in colored_characters:
        text = text.replace(character, '')

    return text


def replace_colors(text):
    """ 
    Replace colored characters
     
    :param text: Text
    :return: New Text
    """

    if text is None:
        return

    minecraft_colors = ['§0', '§1', '§2', '§3', '§4', '§5', '§6', 
                        '§7', '§8', '§9', '§a', '§b', '§c', '§d', 
                        '§e', '§f', '§k', '§l', '§m', '§n', '§o', 
                        '§r', '§A', '§B', '§C', '§D', '§E', '§F', 
                        '§K', '§L', '§M', '§N', '§O', '§R']

    colors = [Fore.LIGHTBLACK_EX, Fore.BLUE, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.RED, 
             Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTBLACK_EX, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, 
             Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTRED_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX, 
             Fore.LIGHTWHITE_EX, '', '', '', '', '', '', Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTRED_EX, 
             Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTWHITE_EX, '', '', '', '', '', '']


    for num, character in enumerate(minecraft_colors):
        text = text.replace(character, colors[int(num)])

    return text