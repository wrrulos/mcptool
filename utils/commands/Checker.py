import re

from utils.alerts.Alerts import alert
from utils.checks.Encoding import check_encoding
from utils.checks.IPPort import check_ip_port
from utils.color.TextColor import paint
from utils.gets.BotArgument import get_bot_argument
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager
from utils.minecraft.CheckServer import check_server


def checker_command(file, bot, proxy=None):
    """ 
    Command that checks if the servers found in a 
    file are turned on.

    Parameters:
    file (str): File containing the servers
    bot (bool): Indicates if a bot will be sent to verify login to the server.
    proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')
    timed_out_servers_found = 0
    servers_found = 0
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
            paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_1"].replace("[0]", str(servers_found))}')

        if settings['SOUNDS']:
            alert('Alert-0')

    except KeyboardInterrupt:
        return