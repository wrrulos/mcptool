import asyncio
import base64
import dns
import re
import requests
import socket

from mcstatus import JavaServer
from utils.mccolor import mcremove, mcreplace

api = 'https://api.mcsrvstat.us/2/'


def mcstatus(server, replace_colors=True, remove_spaces=True):
    """
    Gets the following data from the server:
    > MOTD
    > Version
    > Protocol
    > Connected players / Maximum player limit
    > Player name list (If possible)

    Parameters:
    server: Minecraft server

    Returns:
    str: The data mentioned above
    """

    try:
        srv = JavaServer.lookup(server)
        response = srv.status()

        motd = response.description

        if remove_spaces:
            motd = motd.replace('\n', '')
            motd = re.sub(' +', ' ', motd)

        clean_motd = mcremove(motd)

        if replace_colors:
            motd = mcreplace(motd)

        version = response.version.name

        if remove_spaces:
            version = version.replace('\n', '')
            version = re.sub(' +', ' ', version)

        clean_version = mcremove(version)

        if replace_colors:
            version = mcreplace(version)

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

        data = motd, version, protocol, connected_players, player_limit, players, clean_motd, clean_version, response.players.sample
        return data

    except (OSError, socket.gaierror, socket.timeout, ValueError, IndexError, asyncio.exceptions.TimeoutError, dns.resolver.LifetimeTimeout, dns.resolver.NoNameservers):
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

    Parameters:
    server: Minecraft server

    Returns:
    str: The data mentioned above
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