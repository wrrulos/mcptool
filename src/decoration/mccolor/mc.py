#!/usr/bin/python3

from .ansi import Foreground, Util

colors = ['0', '1', '2', '3', '4',
          '5', '6', '7', '8', '9',
          'a', 'b', 'c', 'd', 'e',
          'f']

codes = {
    '0': Foreground.BLACK,
    '1': Foreground.BLUE,
    '2': Foreground.GREEN,
    '3': Foreground.CYAN,
    '4': Foreground.RED,
    '5': Foreground.MAGENTA,
    '6': Foreground.YELLOW,
    '7': Foreground.LIGHTBLACK_EX,
    '8': Util.DIM + Foreground.LIGHTBLACK_EX,
    '9': Foreground.LIGHTBLUE_EX,
    'a': Foreground.LIGHTGREEN_EX,
    'b': Foreground.LIGHTCYAN_EX,
    'c': Foreground.LIGHTRED_EX,
    'd': Util.BOLD + Foreground.LIGHTMAGENTA_EX,
    'e': Foreground.LIGHTYELLOW_EX,
    'f': Foreground.WHITE,
    'k': '',
    'l': Util.BOLD,
    'm': Util.STRIKETHROUGH,
    'n': Util.UNDERLINE,
    'o': Util.ITALIC,
    'r': Util.RESET_ALL,
    'x': ''
}
