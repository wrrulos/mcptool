import subprocess
import time

from utils.checks.Encoding import check_encoding
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LoopArgument import get_loop_argument
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus


def sendcommand_command(server, username, version, command_file, loop, proxy=None):
    """
    This command runs the SendCommand.js script to send 
    commands with a bot.

    Parameters:
    server (str): IP address and port of the server
    username (str): Bot username
    version (str): Minecraft server version
    command_file (str): File where the commands that the bot will use are located
    loop (bool): Defines if the script will run infinitely.
    proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    with open(command_file, 'r', encoding=check_encoding(command_file)) as f:
        commands = f.readlines()

    if len(commands) == 0:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["sendcmd"]["EMPTY_FILE"]}')
        return
    
    try:
        if mcstatus(server) is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return

    except KeyboardInterrupt:
        return
    
    server = server.split(':')

    if proxy is not None:
        proxy = proxy.split(':')

    command = f'{settings["NODE_COMMAND"]} utils/scripts/SendCommand.js {server[0]} {server[1]} {username} {version} {command_file} {settings["LANGUAGE"]}'
    command += f' {proxy[0]} {proxy[1]}' if proxy is not None else ''
    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["sendcmd"]["STARTING_THE_ATTACK"]}')

    try:
        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)
            
    except KeyboardInterrupt:
        return