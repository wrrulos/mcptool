from utils.banners.banner_messages import *
from utils.banners.print_banner import print_banner


def discord_command():
    """ Command that displays the discord message """

    print_banner(
        'discord',
        discord_message1, 
        discord_message2, 
        discord_message3, 
        discord_message4, 
        discord_message5
    )
