import subprocess

from utils.color.text_color import paint


def print_banner(name, *arguments):
    """
    Open the text file where the banner is located,
    copy it, then replace the arguments (if necessary)

    Args:
        name (str): Banner name
        *arguments (list): Optional arguments
    """

    if 'discord' not in name and 'help' not in name:
        subprocess.run('clear || cls', shell=True)

    file = f'utils/banners/banners/{name}.txt'

    with open(file, 'r', encoding='utf8') as f:
        banner = f.read()

    if arguments is not None:
        for num, argument in enumerate(arguments):
            banner = banner.replace(f'[{num}]', argument)

    paint(banner)
