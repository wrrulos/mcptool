import subprocess
import time

from mcstatus import JavaServer
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LoopArgument import get_loop_argument
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus


def kickall_command(server, version, loop, proxy=None):
    """
    Runs the Kick.js script for each user fetched
    from the server.

    This works if the server allows you to kick another 
    player when you connect from another location.

    Parameters:
    server (str): IP address and port of the server
    version (str): Minecraft server version
    loop (bool): Defines if the script will run infinitely.
    proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    players = []

    # Gets the value of the loop parameter.
    loop = get_loop_argument(loop)

    try:
        if mcstatus(server) is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return
        
        srv = JavaServer.lookup(server)
        response = srv.status()

        if response.players.sample is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kickall"]["NO_PLAYERS"]}')
            return

        for player in response.players.sample:
            players.append(player.name)

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["kickall"]["STARTING_THE_ATTACK"]}')
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