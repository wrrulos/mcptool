#!/usr/bin/python3

import re

from utils.minecraftserver.CheckServer import check_server
from utils.managers.Settings import SettingsManager
from utils.gets.BotArgument import get_bot_argument
from utils.checks.Encoding import check_encoding
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from utils.gets.Language import language
from utils.color.TextColor import paint

sm = SettingsManager()
settings = sm.read('settings')


def checker_command(file, bot, proxy=None):
    """ 
    Command that checks if the servers found in a file are turned on

    :param file: File containing the servers
    :param bot: Boolean value that decides whether to send a bot or not
    :param proxy: Proxy socks5
    """

    f = create_file('checker')
    logs = LogsManager('checker', f)
    bot = get_bot_argument(bot)
    timed_out_servers_found = 0
    servers_found = 0
    server_list = []

    try:
        with open(file, encoding=check_encoding(file)) as f:
            for line in f:
                server = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)
                server = ' '.join(server)

                if ':' in server:
                    server_list.append(server)

        if server_list == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{str(language["commands"]["checker"]["NO_SERVERS_IN_THE_FILE"])}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["checker"]["FOUND_SERVERS"].replace("[0]", str(len(server_list)))}')
        paint(f'\n    {language["script"]["PREFIX"]}{str(language["commands"]["checker"]["CHECKING"])}')
        logs.create(file)

        for server in server_list:
            check = check_server(server, bot, proxy, logs)

            if check is None:
                return

            if check:
                servers_found += 1

            else:
                timed_out_servers_found += 1

        if timed_out_servers_found >= 1:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["checker"]["FINISHED_SCAN_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["checker"]["FINISHED_SCAN_1"].replace("[0]", str(servers_found))}')

        return

    except KeyboardInterrupt:
        return