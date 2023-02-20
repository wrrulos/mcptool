#!/usr/bin/python3

import requests
import base64
import socket
import re

from mcstatus import JavaServer, BedrockServer
from utils.managers.Settings import SettingsManager
from utils.color.ColoredCharacters import remove_colors, replace_colors

api = 'https://api.mcsrvstat.us/2/'
sm = SettingsManager()
settings = sm.read('settings')


def mcstatus(server):
    """
    Gets the following data from the server:
    > MOTD
    > Version
    > Protocol
    > Connected players / Maximum player limit
    > Player name list (If possible)

    :param server: Minecraft Server
    :return: The data mentioned above
    """

    try:
        srv = JavaServer.lookup(server)
        response = srv.status()

        motd = response.description
        motd = motd.replace('\n', '')
        motd = re.sub(' +', ' ', motd)
        clean_motd = remove_colors(motd)
        motd = replace_colors(motd)

        version = response.version.name
        version = version.replace('\n', '')
        version = re.sub(' +', ' ', version)
        clean_version = remove_colors(version)
        version = replace_colors(version)

        protocol = response.version.protocol
        connected_players = response.players.online
        player_limit = response.players.max

        if response.players.sample is not None:
            players = str([f'{player.name} ({player.id})' for player in response.players.sample])
            players = players.replace('[', ''
                            ).replace(']', ''
                            ).replace("'", ''
                            ).replace('(00000000-0000-0000-0000-000000000000),', ''
                            ).replace('(00000000-0000-0000-0000-000000000000)', '')
                            
            re.findall(r'[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z]-[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z]', players)

        else: 
            players = None

        data = motd, version, protocol, connected_players, player_limit, players, clean_motd, clean_version
        return data

    except (OSError, socket.gaierror, socket.timeout, ValueError, IndexError):
        return None


def mcsrvstatus(server):
    """
    Gets the following data from the server using mcsrvstatus api:

    > IP
    > Port
    > MOTD
    > Version
    > Protocol
    > Connected players / Maximum player limit
    > Icon

    :param server: Minecraft Server
    :return: The data mentioned above
    """

    try:
        r = requests.get(f'{api}{server}')
        r_json = r.json()

    except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError):
        return None

    try:
        online_players = r_json['players']['online']
        max_players = r_json['players']['max']
        motd = r_json['motd']['raw']
        ip = r_json['ip'] 
        port = r_json['port']

    except KeyError:
        return None

    try:
        icon = r_json['icon']
        data = icon.replace('data:image/png;base64,', '')
        image = base64.b64decode(data)

    except KeyError:
        image = None

    data = ip, port, motd, online_players, max_players, image
    return data