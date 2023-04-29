import requests
import random
import re

from utils.alerts.Alerts import alert
from utils.color.TextColor import paint
from utils.gets.BotArgument import get_bot_argument
from utils.gets.Headers import get_headers
from utils.gets.IPAndPort import get_ip_port
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager
from utils.minecraft.CheckServer import check_server


def aternos_command(pages, bot, proxy=None):
    """
    Get Minecraft servers by reading Aternos 
    page HTML code.
        
    Parameters:
        pages (str): Number of pages where servers will be searched.
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    url = 'https://board.aternos.org/board/90-serverlist/?pageNo='
    regex = '<a href="https://board.aternos.org/thread/(.*?)/"'
    servers_found = 0
    timed_out_servers_found = 0
    servers = []

    # Gets the value of the Bot parameter.
    bot = get_bot_argument(bot)

    # Get a list of headers to use.
    headers_list = get_headers()
    cookies = {'cookie_name': 'cookie_value'}

    # Create a file to save the logs.
    file = create_file('aternos')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('aternos', file)
    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["aternos"]["GET_SERVERS"]}')
    
    for num in range(0, int(pages)):
        page = f'{url}{num}'
        headers = headers_list[random.randint(0, len(headers_list)-1)]

        try:
            text = requests.get(page, headers=headers, cookies=cookies, timeout=5).text

        except requests.exceptions.ReadTimeout:
            continue

        publications = re.findall(regex, text)
        page = page.replace(f'board/90-serverlist/?pageNo={num}', 'thread')

        for publication in publications:
            publication = f'{page}/{publication}'

            try:
                text = requests.get(publication, headers=headers, cookies=cookies, timeout=5).text
            
            except requests.exceptions.ReadTimeout:
                continue
            
            results = re.findall(r'<dd>(.*?)</dd>', text)

            if len(results) >= 1:
                for result in results:
                    if len(result) > 5:
                        if result not in servers:
                            if not result.startswith('<a href="'):
                                servers.append(result)
                                break

    if not servers:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["aternos"]["SERVERS_NOT_FOUND"]}')
        return

    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["aternos"]["CHECKING_SERVERS"].replace("[0]", str(len(servers)))}')
    logs.create(pages)

    for server in servers: 
        if bot:
            ip, port = get_ip_port(server)
            server = f'{ip}:{port}'

        check = check_server(server, bot, proxy, logs, timeout=False)

        if check is None:
            return

        if check:
            servers_found += 1

        else:
            timed_out_servers_found += 1

    if settings['SHOW_TIMED_OUT_SERVERS'] and timed_out_servers_found >= 1:
        paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

    else:
        paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_1"].replace("[0]", str(servers_found))}')

    if settings['SOUNDS']:
        alert('Alert-0')
