#!/usr/bin/python3

from utils.banners.PrintBanner import print_banner
from utils.gets.Language import language


def discord_command():
    """ 
    Command that displays the discord message
    """
    
    message1 = language['banners']['discord']['MESSAGE1']
    message2 = language['banners']['discord']['MESSAGE2']
    message3 = language['banners']['discord']['MESSAGE3']
    message4 = language['banners']['discord']['MESSAGE4']
    message5 = language['banners']['discord']['MESSAGE5']
    print_banner('discord', message1, message2, message3, message4, message5)