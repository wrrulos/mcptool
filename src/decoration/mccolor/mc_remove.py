#!/usr/bin/python3

from .mc import codes


def mcremove(text):
    """
    Allows you to remove color codes from a text.

    :param text: Text
    :return: Clean text
    """

    for code in codes.items():
        text = text.replace(f'&{code[0]}', ''
                  ).replace(f'§{code[0]}', '')
    
    return text
