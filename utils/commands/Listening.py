#!/usr/bin/python3

# This command allows you to listen to users who enter the server.

import socket
import time

from utils.minecraftserver.ServerData import mcstatus
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from utils.gets.Language import language
from utils.color.TextColor import paint
from mcstatus import JavaServer


def listening_command(server):
    """ 
    Save all players that enter the server 
    
    :param server: IP address and port
    """

    file = create_file('listening')
    logs = LogsManager('listening', file)
    player_list = []
    found = False

    try:
        data = mcstatus(server)

        if data is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["listening"]["INVALID_SERVER"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["listening"]["WAITING_FOR_PLAYERS"]}')

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
                            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["listening"]["FOUND_PLAYERS"]}\n')
                            found = True

                        if f'{player.name} ({player.id})' not in player_list:
                            player_found = f'{player.name} ({player.id})'
                            player_list.append(player_found)
                            player_found = f'[lwhite]{player.name} [lwhite]([lgreen]{player.id}[lwhite])'
                            paint(f'     [lred]• {player_found}')
                            logs.write('save_player', player_found)

            time.sleep(1)

        except (socket.gaierror, socket.timeout):
            time.sleep(30)

        except KeyboardInterrupt:
            return
