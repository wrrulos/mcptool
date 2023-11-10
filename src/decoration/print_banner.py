import subprocess

from src.decoration.paint import paint


def print_banner(name, *arguments):
    """
    Display a banner by reading its content from a text file and replacing placeholders with arguments.

    This function reads the content of a banner text file based on the provided 'name', 
    and if optional 'arguments' are provided, it replaces placeholders in the banner text 
    with those arguments before displaying it.

    Args:
        name (str): Banner name.
        *arguments (list): Optional arguments to replace placeholders in the banner.
    """

    # Clear the console screen if the banner is not for Discord or help.
    if 'discord' not in name and 'help' not in name:
        subprocess.run('clear || cls', shell=True)

    # Construct the file path to the banner text file.
    file = f'./mcptool_files/banners/{name}.txt'

    # Read the content of the banner text file.
    with open(file, 'r', encoding='utf8') as f:
        banner = f.read()

    # Replace placeholders in the banner text with provided arguments (if any).
    if arguments is not None:
        for num, argument in enumerate(arguments):
            banner = banner.replace(f'[{num}]', argument)

    # Display the banner.
    paint(banner)