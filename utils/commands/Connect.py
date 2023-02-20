#!/usr/bin/python3

import subprocess

from utils.minecraftserver.ServerData import mcstatus
from utils.managers.Settings import SettingsManager
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def connect_command(server, username, version, proxy=None):
    """ 
    This command sends a bot to the specified server using 
    the Connect.js script.
    
    :param server: IP address and port of the server
    :param username: Username that the bot will have
    :param protocol: Protocol number or version
    """

    if mcstatus(server) is None:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["connect"]["INVALID_SERVER"]}')
        return

    server = server.split(':')

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Connect.js {server[0]} {server[1]} {username} {version} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}')

        else:
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Connect.js {server[0]} {server[1]} {username} {version} {settings["LANGUAGE"]}')

    except KeyboardInterrupt:
        return