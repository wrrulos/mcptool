import subprocess

from utils.gets.BotUsername import get_bot_username
from utils.managers.Settings import SettingsManager
from utils.minecraft.CheckProtocol import check_protocol


def send_bot(server, protocol, proxy):
    """ 
    This function runs the Checker.js script and saves the 
    output of the command. 
    
    This output will show if the connection to the server was successful.

    Parameters:
    server (str): Server IP address and port
    protocol (str): Server Protocol
    bot (bool): Indicates if a bot will be sent to verify login to the server.
    proxy (str): Optional proxy to use for the bot.
        
    Returns:
    str: The output of the command
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    if not check_protocol(str(protocol)):
        return f'§4Protocol §c{str(protocol)} §4is not supported'

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