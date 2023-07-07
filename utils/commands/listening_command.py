import socket
import time

from mcstatus import JavaServer
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.gets.get_player_uuid_color import uuid_color
from utils.managers.logs_manager import LogsManager
from utils.minecraft.active_server import active_server
from utils.gets.get_spaces import get_spaces


def listening_command(server):
    """ 
    Listen to the people who enter the server. 
    Saves the name and uuid of the player.

    Args:
        server (str): IP Address and Port
    """

    players = []
    found = False
    t = ''

    # Create a file to save the logs.
    file = create_file('listening')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('listening', file)

    try:
        if not active_server(server):
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["listening"]["waitingForPlayers"]}\n')

    except KeyboardInterrupt:
        return

    logs.create(server)

    while True:
        try:
            srv = JavaServer.lookup(server)
            response = srv.status()

            if response.players.sample is not None:
                for player in response.players.sample:
                    if player.name != '':
                        if not found:
                            paint(f'{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["listening"]["foundPlayers"]}\n')
                            t = '\n'
                            found = True

                        if f'{player.name} ({player.id})' not in players:
                            player_found = f'{player.name} ({player.id})'
                            players.append(player_found)
                            player_found = f'&f&l{player.name} &f&l({uuid_color(player.name, player.id)}{player.id}&f&l)'
                            paint(f'{get_spaces()}&c• {player_found}')
                            logs.write('save_player', player_found)

            time.sleep(1)

        except (socket.gaierror, socket.timeout, OSError):
            time.sleep(30)

        except KeyboardInterrupt:
            paint(f'{t}    {language_manager.language["prefix"]}{language_manager.language["stopping"]}')
            return
