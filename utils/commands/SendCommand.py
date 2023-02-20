#!/usr/bin/python3

import subprocess

from utils.minecraftserver.ServerData import mcstatus
from utils.managers.Settings import SettingsManager
from utils.checks.Encoding import check_encoding
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def sendcommand_command(server, username, version, command_file, proxy=None):
    """
    This command performs a brute force attack to guess the 
    password of the non-premium user on the specified server. 
    
    For this use the Auth.js script

    :param server: IP address and port of the server
    :param username: Username that the bot will have
    :param version: Minecraft server version
    :param command_file: File where the commands that the bot will use are located
    :param proxy: In the event that a user has entered a proxy, the bot will connect to the proxy.
    """

    try:
        if mcstatus(server) is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["sendcommand"]["INVALID_SERVER"]}')
            return

        with open(command_file, 'r', encoding=check_encoding(command_file)) as f:
            commands = f.readlines()

        if len(commands) == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["sendcommand"]["EMPTY_FILE"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["sendcommand"]["STARTING_THE_ATTACK"]}')
        server = server.split(':')

        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/SendCommand.js {server[0]} {server[1]} {username} {version} {command_file} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', shell=True)

        else:
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/SendCommand.js {server[0]} {server[1]} {username} {version} {command_file} {settings["LANGUAGE"]}', shell=True)
        
    except KeyboardInterrupt:
        return