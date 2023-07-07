import random
import re
import requests

from utils.color.text_color import paint
from utils.gets.get_bot_argument import get_bot_argument
from utils.gets.get_headers import get_headers
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.managers.logs_manager import LogsManager
from utils.minecraft.check_servers import check_servers
from utils.gets.get_spaces import get_spaces


def websearch_command(tag, bot=False, proxy_file=None):
    """
    Get minecraft servers by reading the HTML 
    code of known pages.
        
    Args:
        tag (str): Tag to use in the pages.
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy_file (str): Optional proxy to use for the bot.
    """

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
    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["websearch"]["searching"].replace("[0]", tag)}')
    
    try:
        for url in urls.items():
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["websearch"]["webSearch"].replace("[0]", url[0])}')

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
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["websearch"]["serversNotFound"]}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["websearch"]["checkingServers"].replace("[0]", str(len(servers)))}')
        logs.create(tag)
        check_servers(servers, bot, proxy_file, logs)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
