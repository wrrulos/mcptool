import re

from utils.checks.check_encoding import check_encoding
from utils.checks.check_ip_port import check_ip_port
from utils.color.text_color import paint
from utils.gets.get_bot_argument import get_bot_argument
from utils.gets.get_log_file import create_file
from utils.managers.logs_manager import LogsManager
from utils.managers.language_manager import language_manager
from utils.minecraft.check_servers import check_servers
from utils.gets.get_spaces import get_spaces


def checker_command(file, bot=False, proxy_file=None):
    """ 
    Command that checks if the servers found in a 
    file are turned on.

    Args:
        file (str): File containing the servers
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy_file (str): Optional proxy to use for the bot.
    """

    server_list = []

    # Gets the value of the Bot parameter.
    bot = get_bot_argument(bot)
    
    # Create a file to save the logs.
    f = create_file('checker')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('checker', f)

    try:
        with open(file, encoding=check_encoding(file)) as f:
            for line in f:
                servers = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

                for server in servers:
                    if check_ip_port(server):
                        server_list.append(server)

        if len(server_list) == 0:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{str(language_manager.language["commands"]["checker"]["noServersInTheFile"])}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["checker"]["foundServers"].replace("[0]", str(len(server_list)))}')
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{str(language_manager.language["commands"]["checker"]["checking"])}')
        logs.create(file)
        check_servers(server_list, bot, proxy_file, logs)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
