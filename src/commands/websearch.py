import random
import re
import requests

from src.decoration.paint import paint
from src.utilities.get_utilities import GetUtilities
from src.managers.json_manager import JsonManager
from src.managers.log_manager import LogManager
from src.minecraft.show_minecraft_server import show_server
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData


def websearch_command(tag, *args):
    """
    Get Minecraft servers by reading the HTML code of known pages.

    Args:
        tag (str): Tag to use in the pages.
        *args: Additional arguments.

    This function searches for Minecraft servers on specific websites by reading their HTML code.
    It collects server information based on the specified tag and displays it on the screen.
    Servers that match the criteria are logged for future reference.
    """

    servers = []
    servers_found = 0

    log_file = LogManager.create_log_file('websearch')

    # Dictionary of pages and how to find the servers.
    urls = {
        'https://servers-minecraft.net': '<div class=".*?"><span>(.*?)</span>',
        'https://minecraftservers.org': '<p><span class="icon ip"></span>(.*?)</p>',
        'https://minecraft-mp.com': '<strong>(.*?)</strong></button>',
    }

    # Get a list of headers to use.
    headers_list = GetUtilities.get_headers()
    cookies = {'cookie_name': 'cookie_value'}

    # Words that should not appear.
    invalid_words = ['playing now', 'Copy IP', '#']

    # Display a message indicating that the web search is starting.
    paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "searching"]).replace("[0]", tag)}')

    try:
        for url in urls.items():
            # Iterate through the specified websites.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "webSearch"]).replace("[0]", url[0])}')

            for num in range(1, 500):
                # Iterate through pages of each website.
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
                    # Send an HTTP request to the page.
                    headers = headers_list[random.randint(0, len(headers_list) - 1)]
                    text = requests.get(page, headers=headers, cookies=cookies, timeout=5).text

                except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                    # Handle a timeout for the HTTP request.
                    break

                # Check for specific conditions to determine if the page should be skipped.
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

                # Extract server information based on the specified HTML pattern.
                server_list = re.findall(url[1], text)

                # Check and filter server information.
                for server in server_list:
                    if server not in servers:
                        for word in invalid_words:
                            if word in server:
                                break

                        else:
                            servers.append(server)

                continue

        # Check if any servers were found.
        if not servers:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "serversNotFound"])}')
            return

        # Display a message indicating that the servers are being checked.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "websearch", "checkingServers"]).replace("[0]", str(len(servers)))}')

        for server in servers:
            # Retrieve and display detailed information about each server.
            server_data = GetMinecraftServerData.get_data(server)

            if server_data is not None:
                show_server(server_data)
                servers_found += 1

                if JsonManager.get('logs'):
                    # Prepare server data for logging and write it to the log file.
                    log_data = list(server_data.values())
                    LogManager.write_log(log_file, 'websearch', log_data)
        
        if servers_found >= 1:
            # Display the number of Minecraft servers found.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversFound"]).replace("[0]", str(servers_found))}')

        else:
            # Display a message when no Minecraft servers are found.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversNotFound"])}')
                    
    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt (Ctrl+C) gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
