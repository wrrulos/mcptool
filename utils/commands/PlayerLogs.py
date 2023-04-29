import datetime
import re
import socket
import time

from mcstatus import JavaServer
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.gets.PlayerUUIDColor import uuid_color
from utils.managers.Logs import LogsManager
from utils.minecraft.ServerData import mcstatus


def playerlogs_command(server):
    """ 
    Listen to the people who enter the server. 
    Saves the name and uuid of the player.

    Parameters:
        server (str): IP Address and Port
    """

    old_players = []
    players = []
    regex = r'\((.*?)\)'
    t = ''

    # Create a file to save the logs.
    file = create_file('playerlogs')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('playerlogs', file)

    try:
        data = mcstatus(server)

        if data is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["playerlogs"]["WAITING_FOR_PLAYERS"]}\n')

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
                user = player.split(" (")[0]
                uuid = re.search(regex, player).group(1)
                data = f'{user} &f&l({uuid_color(user, uuid)}{uuid}&f&l)'
                logs.write('save_player_log', current_time, f'- {data}')
                paint(f'    {language["commands"]["playerlogs"]["DISCONNECTED_USER"].replace("[0]", current_time).replace("[1]", data)}')

            for player in added_players:
                user = player.split(" (")[0]
                uuid = re.search(regex, player).group(1)
                data = f'{user} &f&l({uuid_color(user, uuid)}{uuid}&f&l)'
                logs.write('save_player_log', current_time, f'+ {data}')
                paint(f'    {language["commands"]["playerlogs"]["CONNECTED_USER"].replace("[0]", current_time).replace("[1]", data)}')
                players.append(player)

            old_players = players
            time.sleep(1)

        except (socket.gaierror, socket.timeout, OSError):
            time.sleep(30)

        except KeyboardInterrupt:
            paint(f'{t}    {language["script"]["PREFIX"]}{language["other_messages"]["STOPPING"]}')
            return
