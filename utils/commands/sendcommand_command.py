import subprocess
import time

from utils.checks.check_encoding import check_encoding
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_loop_argument import get_loop_argument
from utils.managers.config_manager import config_manager
from utils.minecraft.active_server import active_server
from utils.gets.get_spaces import get_spaces


def sendcommand_command(server, username, version, command_file, loop, proxy_file=None):
    """
    This command runs the SendCommand.js script to send 
    commands with a bot.

    Args:
        server (str): IP address and port of the server
        username (str): Bot username
        version (str): Minecraft server version
        command_file (str): File where the commands that the bot will use are located
        loop (bool): Defines if the script will run infinitely.
        proxy_file (str): Optional proxy_file to use for the bot.
    """

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    with open(command_file, 'r', encoding=check_encoding(command_file)) as f:
        commands = f.readlines()

    if len(commands) == 0:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["sendcmd"]["emptyFile"]}')
        return
    
    try:
        if not active_server(server):
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return

    except KeyboardInterrupt:
        return
    
    server = server.split(':')

    if proxy_file is not None:
        proxy_file = proxy_file.split(':')

    command = f'{config_manager.config["commands"]["nodejs"]} utils/scripts/sendcmd.js {server[0]} {server[1]} {username} {version} {command_file} {len(get_spaces())} '
    command += proxy_file if proxy_file is not None else ''
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["sendcmd"]["startingTheAttack"]}')

    try:
        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)
            
    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
