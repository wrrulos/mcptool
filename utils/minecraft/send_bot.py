import subprocess

from utils.managers.config_manager import config_manager


def send_bot(server, protocol, proxy_file):
    """ 
    This function runs the checker.js script and saves the
    output of the command. 
    
    This output will show if the connection to the server was successful.

    Args:
        server (str): Server IP address and port
        protocol (str): Server Protocol
        proxy_file (str): Optional proxy file to use for the bot.
        
    Returns:
        str: The output of the command
    """

    try:
        server = server.split(':')

        if proxy_file is not None:
            result = subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/checker.js {server[0]} {server[1]} {protocol} {proxy_file}', stdout=subprocess.PIPE, encoding='utf-8', shell=True)

        else:
            result = subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/checker.js {server[0]} {server[1]} {protocol}', stdout=subprocess.PIPE, encoding='utf-8', shell=True)

        output = result.stdout
        return output

    except KeyboardInterrupt:
        return None
