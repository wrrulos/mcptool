import json
import requests
import shodan

from utils.minecraft.check_servers import check_servers
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.managers.logs_manager import LogsManager
from utils.managers.config_manager import config_manager
from utils.gets.get_spaces import get_spaces


def search_command(*data):
    """
    Use the Shodan search engine to search for IP addresses 
    that have port 25565 open and then check if they are 
    from Minecraft, to finally show it on the screen. 

    Args:
        data (str): Data that will be used to search for servers.
    """

    server_list = []

    if config_manager.config['shodanApiKey'] == '':
        paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["shodanInvalidApiKey"]}')
        return

    # Join the elements of the list "data" in a string separated by spaces.
    data = ' '.join(str(i) for i in data)

    # Create a file to save the logs.
    file = create_file('search')
    
    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('search', file)

    # Separate the data.
    data = data.split(' --- ')

    try:
        search = shodan.Shodan(config_manager.config['shodanApiKey'])
        all_data = ''
        
        # Separates the data entered by the user.
        for i in data:
            all_data = f'{all_data}{i} '
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["search"]["scanning"]} &a{i}')
            servers = search.search(i)

            for server in servers['matches']:
                server_list.append(f'{str(server["ip_str"])}:{str(server["port"])}')

        if len(server_list) >= 1:
            server_list = list(set(server_list))
            message_found_ips = str(language_manager.language["commands"]["search"]["ipsFound"]).replace('[0]', str(len(server_list))).replace('[1]', all_data[:-1])
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{message_found_ips}')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["search"]["serversNotFound"]} &f&l(&a{all_data[:-1]}&f&l)')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["search"]["checkingServers"]}')
        logs.create(all_data)
        check_servers(server_list, False, None, logs)

    except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError, KeyboardInterrupt):
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return

    except shodan.exception.APIError as e:
        if 'Invalid API key' in str(e):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["shodanInvalidApiKey"]}')

        elif 'Access denied' in str(e):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["shodanApiKeyNoAccess"]}')
        
        else:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}&f&lThe connection to the Shodan API could not be established.')

        return
