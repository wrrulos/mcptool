import subprocess
import time

from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_loop_argument import get_loop_argument
from utils.managers.config_manager import config_manager
from utils.minecraft.active_server import active_server
from utils.gets.get_spaces import get_spaces


def kick_command(server, username, version, loop, proxy_file=None):
    """
    Runs the kick.js script to kick the specified
    player from the selected server.

    This works if the server allows you to kick another 
    player when you connect from another location.

    Args:
        server (str): IP address and port of the server
        username (str): Bot username
        version (str): Minecraft server version
        loop (bool): Defines if the script will run infinitely.
        proxy_file (str): Optional proxy_file to use for the bot.
    """

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    if not active_server(server):
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
        return
    
    server = server.split(':')
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["kick"]["startingTheAttack"]}')

    # Set the command.
    command = f'{config_manager.config["commands"]["nodejs"]} utils/scripts/kick.js {server[0]} {server[1]} {username} {version} '
    command += proxy_file if proxy_file is not None else ''

    try:
        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
