import subprocess

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus


def connect_command(server, username, version, proxy=None):
    """ 
    Run the Connect.js script. 
    This script allows to control a bot from the terminal
    
    Parameters:
        server (str): IP address and port of the server
        username (str): Bot username
        protocol (str): Protocol number or version
        proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    if mcstatus(server) is None:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
        return

    server = server.split(':')

    try:
        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Connect.js {server[0]} {server[1]} {username} {version} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', shell=True)

        else:
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Connect.js {server[0]} {server[1]} {username} {version} {settings["LANGUAGE"]}', shell=True)

    except KeyboardInterrupt:
        return
