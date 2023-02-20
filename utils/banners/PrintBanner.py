#!/usr/bin/python3

import subprocess

from utils.color.TextColor import paint


def print_banner(name, *arguments):
    """
    Open the text file where the banner is located,
    copy it, then replace the arguments (if necessary)

    :param name: Banner Name
    :param *arguments: Optional arguments
    """

    if not 'discord' in name and not 'help' in name:
        subprocess.run('cls || clear', shell=True)

    file = f'utils/banners/banners/{name}.txt'

    with open(file, 'r', encoding='utf8') as f:
        banner = f.read()

    if arguments is not None:
        for num, argument in enumerate(arguments):
            banner = banner.replace(f'[{num}]', argument)

    paint(banner)
