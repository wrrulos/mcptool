import random
import re
import requests

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


def websearch_command(tag, bot, proxy=None):
    """
    Get minecraft servers by reading the HTML 
    code of known pages.
        
    Parameters:
        tag (str): Tag to use in the pages.
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    servers_found = 0
    timed_out_servers_found = 0
    servers = []

    # Dictionary of pages and how to find the servers.
    urls = {
        'https://servers-minecraft.net': '<div class=".*?"><span>(.*?)</span>',
        'https://minecraftservers.org': '<p><span class="icon ip"></span>(.*?)</p>',
        'https://minecraft-mp.com': '<strong>(.*?)</strong></button>',
    }

    # Gets the value of the Bot parameter.
    bot = get_bot_argument(bot)

    # Get a list of headers to use.
    headers_list = get_headers()
    cookies = {'cookie_name': 'cookie_value'}

    # Create a file to save the logs.
    file = create_file('websearch')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('websearch', file)

    # Words that should not appear.
    invalid_words = ['playing now', 'Copy IP', '#']
    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["websearch"]["SEARCHING"].replace("[0]", tag)}')
    
    try:
        for url in urls.items():
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["websearch"]["WEB_SEARCH"].replace("[0]", url[0])}')

            for num in range(1, 500):
                page = url[0]

                if page == 'https://minecraft-mp.com':
                    page = f'{page}/type/{tag.lower()}'
                    page = f'{page}/{num}/'

                elif page == 'https://servers-minecraft.net':
                    page = f'{page}/minecraft-{tag.lower()}-servers'
                    page = f'{page}/pg.{num}'

                elif page == 'https://minecraftservers.org':
                    page = f'{page}/search/{tag}'
                    page = f'{page}/{num}'

                try:
                    headers = headers_list[random.randint(0, len(headers_list)-1)]
                    text = requests.get(page, headers=headers, cookies=cookies, timeout=5).text

                except requests.exceptions.ReadTimeout:
                    break

                if 'https://minecraft-mp.com/' in page:
                    if '<h1>Minecraft Servers By Types</h1>' in text:
                        break

                    if not ', page' in text and num > 1:
                        break

                if 'https://minecraftservers.org' in page:
                    if '<p>Found 0 servers</p>' in text:
                        break

                    if '<title>404 Page Not Found | Minecraft Servers' in text:
                        break

                if 'https://servers-minecraft.net' in page:
                    if '<span>No Servers</span>' in text:
                        break

                server_list = re.findall(url[1], text)

                for server in server_list:
                    if server not in servers:
                        for word in invalid_words:
                            if word in server:
                                break

                        else:
                            servers.append(server)

                continue

        if not servers:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["websearch"]["SERVERS_NOT_FOUND"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["websearch"]["CHECKING_SERVERS"].replace("[0]", str(len(servers)))}')
        logs.create(tag)

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

    except KeyboardInterrupt:
        return
