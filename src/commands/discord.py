from src.decoration.paint import paint
from src.decoration.print_banner import print_banner
from src.utilities.check_utilities import CheckUtilities
from src.utilities.get_utilities import GetUtilities


def discord_command(*args):
    """
    Display a banner with information about Discord integration.

    Args:
        *args: Additional arguments (not used in this function).
    """

    if CheckUtilities.check_termux():
        # Display a Termux-specific message in the terminal.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["banners", "discord", "termux_message"])}')

    else:
        # Display a banner with information about Discord integration.
        print_banner('discord', GetUtilities.get_translated_text(['banners', 'discord', 'message1']),
                     GetUtilities.get_translated_text(['banners', 'discord', 'message2']),
                     GetUtilities.get_translated_text(['banners', 'discord', 'message3']),
                     GetUtilities.get_translated_text(['banners', 'discord', 'message4']),
                     GetUtilities.get_translated_text(['banners', 'discord', 'message5']))
