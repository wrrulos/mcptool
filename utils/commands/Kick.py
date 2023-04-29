import subprocess
import time

from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LoopArgument import get_loop_argument
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus


def kick_command(server, username, version, loop, proxy=None):
    """
    Runs the Kick.js script to kick the specified 
    player from the selected server.

    This works if the server allows you to kick another 
    player when you connect from another location.

    Parameters:
        server (str): IP address and port of the server
        username (str): Bot username
        version (str): Minecraft server version
        loop (bool): Defines if the script will run infinitely.
        proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    if mcstatus(server) is None:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
        return
    
    server = server.split(':')

    if proxy is not None:
        proxy = proxy.split(':')

    command = f'{settings["NODE_COMMAND"]} utils/scripts/Kick.js {server[0]} {server[1]} {username} {version} {settings["LANGUAGE"]}'
    command += f' {proxy[0]} {proxy[1]}' if proxy is not None else ''
    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kick"]["STARTING_THE_ATTACK"]}')

    try:
        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        return
