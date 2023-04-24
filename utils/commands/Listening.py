import socket
import time

from mcstatus import JavaServer
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.gets.PlayerUUIDColor import uuid_color
from utils.managers.Logs import LogsManager
from utils.minecraft.ServerData import mcstatus


def listening_command(server):
    """ 
    Listen to the people who enter the server. 
    Saves the name and uuid of the player.

    Parameters:
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
        data = mcstatus(server)

        if data is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["listening"]["WAITING_FOR_PLAYERS"]}\n')

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
                            paint(f'    {language["script"]["PREFIX"]}{language["commands"]["listening"]["FOUND_PLAYERS"]}\n')
                            t = '\n'
                            found = True

                        if f'{player.name} ({player.id})' not in players:
                            player_found = f'{player.name} ({player.id})'
                            players.append(player_found)
                            player_found = f'&f&l{player.name} &f&l({uuid_color(player.name, player.id)}{player.id}&f&l)'
                            paint(f'     &c• {player_found}')
                            logs.write('save_player', player_found)

            time.sleep(1)

        except (socket.gaierror, socket.timeout, OSError):
            time.sleep(30)

        except KeyboardInterrupt:
            paint(f'{t}    {language["script"]["PREFIX"]}{language["other_messages"]["STOPPING"]}')
            return
