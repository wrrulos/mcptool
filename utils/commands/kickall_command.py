import subprocess
import time

from mcstatus import JavaServer
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_loop_argument import get_loop_argument
from utils.managers.config_manager import config_manager
from utils.minecraft.active_server import active_server
from utils.gets.get_spaces import get_spaces


def kickall_command(server, version, loop, proxy_file=None):
    """
    Runs the kick.js script for each user fetched
    from the server.

    This works if the server allows you to kick another 
    player when you connect from another location.

    Args:
        server (str): IP address and port of the server
        version (str): Minecraft server version
        loop (bool): Defines if the script will run infinitely.
        proxy_file (str): Optional proxy_file to use for the bot.
    """

    players = []

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    try:
        if not active_server(server):
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return
        
        srv = JavaServer.lookup(server)
        response = srv.status()

        if response.players.sample is None:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["kickall"]["noPlayers"]}')
            return

        for player in response.players.sample:
            players.append(player.name)

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["kickall"]["startingTheAttack"]}')
        server = server.split(':')

        if loop:
            while True:
                time.sleep(2)
                for player in players:
                    # Set the command.
                    command = f'{config_manager.config["commands"]["nodejs"]} utils/scripts/kick.js {server[0]} {server[1]} {player} {version} '
                    command += proxy_file if proxy_file is not None else ''
                    subprocess.run(command, shell=True)
            
        else:
            for player in players:
                # Set the command.
                command = f'{config_manager.config["commands"]["nodejs"]} utils/scripts/kick.js {server[0]} {server[1]} {player} {version} '
                command += proxy_file if proxy_file is not None else ''
                subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
