#!/usr/bin/python3

import subprocess

from utils.managers.Settings import SettingsManager
from utils.gets.BotUsername import get_bot_username

sm = SettingsManager()
settings = sm.read('settings')


def send_bot(server, protocol, proxy):
    """ 
    This function runs the Checker.js script and saves the 
    output of the command. 
    
    This output will show if the connection to the server was successful.

    :param server: Server IP address and port
    :param protocol: Server Protocol
    :param proxy: In the event that a user has entered a proxy, the bot will connect to the proxy.
    :return: The output of the command
    """

    try:
        username = get_bot_username()
        server = server.split(':')

        if proxy is not None:
            proxy = proxy.split(':')
            result = subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Checker.js {server[0]} {server[1]} {username} {protocol} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', stdout=subprocess.PIPE, encoding='utf-8')

        else:
            result = subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/Checker.js {server[0]} {server[1]} {username} {protocol} {settings["LANGUAGE"]}', stdout=subprocess.PIPE, encoding='utf-8')

        output = result.stdout
        return output

    except KeyboardInterrupt:
        return None