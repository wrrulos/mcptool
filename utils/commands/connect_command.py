import subprocess

from utils.color.text_color import paint
from utils.managers.config_manager import config_manager
from utils.managers.language_manager import language_manager
from utils.minecraft.server_data import GetDataFromMinecraftServer
from utils.gets.get_spaces import get_spaces


def connect_command(server, username, version, proxy_file=None):
    """ 
    Run the connect.js script.
    This script allows to control a bot from the terminal
    
    Args:
        server (str): IP address and port of the server
        username (str): Bot username
        version (str): Protocol number or version
        proxy_file (str): Optional proxy to use for the bot.
    """

    server_data = GetDataFromMinecraftServer(server)
    data = server_data.get_information()

    if data is None:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
        return

    server = server.split(':')

    try:
        if proxy_file is not None:
            subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/connect.js {server[0]} {server[1]} {username} {version} {len(get_spaces())}{proxy_file}', shell=True)

        else:
            subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/connect.js {server[0]} {server[1]} {username} {version} {len(get_spaces())}', shell=True)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
