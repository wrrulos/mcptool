import datetime
import re
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


def playerlogs_command(server):
    """ 
    Listen to the people who enter the server. 
    Saves the name and uuid of the player.

    Args:
        server (str): IP Address and Port
    """

    old_players = []
    regex = r'\((.*?)\)'
    t = ''

    # Create a file to save the logs.
    file = create_file('playerlogs')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('playerlogs', file)

    try:
        if not active_server(server):
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["playerlogs"]["waitingForPlayers"]}\n')

    except KeyboardInterrupt:
        return

    logs.create(server)

    while True:
        try:
            srv = JavaServer.lookup(server)
            response = srv.status()
            players = []

            if response.players.sample is not None:
                for player in response.players.sample:
                    if player.name != '':
                        player_found = f'{player.name} ({player.id})'
                        players.append(player_found)
                        t = '\n'

            removed_players = set(old_players) - set(players)
            added_players = set(players) - set(old_players)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for player in removed_players:
                user = player.split(' (')[0]
                uuid = re.search(regex, player).group(1)
                data = f'{user} &f&l({uuid_color(user, uuid)}{uuid}&f&l)'
                logs.write('save_player_log', current_time, f'- {data}')
                paint(f'{get_spaces()}{language_manager.language["commands"]["playerlogs"]["disconnectedUser"].replace("[0]", current_time).replace("[1]", data)}')

            for player in added_players:
                user = player.split(" (")[0]
                uuid = re.search(regex, player).group(1)
                data = f'{user} &f&l({uuid_color(user, uuid)}{uuid}&f&l)'
                logs.write('save_player_log', current_time, f'+ {data}')
                paint(f'{get_spaces()}{language_manager.language["commands"]["playerlogs"]["connectedUser"].replace("[0]", current_time).replace("[1]", data)}')
                players.append(player)

            old_players = players
            time.sleep(1)

        except (socket.gaierror, socket.timeout, OSError):
            time.sleep(30)

        except KeyboardInterrupt:
            paint(f'{t}    {language_manager.language["prefix"]}{language_manager.language["stopping"]}')
            return
