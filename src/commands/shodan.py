import shodan
import requests
import json

from src.decoration.paint import paint
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities
from src.minecraft.show_minecraft_server import show_server
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.log_manager import LogManager


def shodan_command(*data):
    """
    Search for Minecraft servers using Shodan.

    Args:
        *data: A list of search terms for Minecraft servers.

    This function searches for Minecraft servers using the Shodan API based on provided search terms.
    It retrieves server information, displays found servers, and logs the results.
    """
    
    server_list = []
    servers_found = 0

    if JsonManager.get(['shodanApiKey']) == '':
        # Check if a Shodan API key is provided.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanInvalidApiKey"])}')
        return

    # Join the elements of the list "data" into a single string separated by spaces.
    data = ' '.join(str(i) for i in data)

    # Split the combined data into individual search terms.
    data = data.split(' --- ')

    try:
        # Initialize the Shodan search with the provided API key.
        search = shodan.Shodan(JsonManager.get(['shodanApiKey']))
        all_data = ''

        for i in data:
            # Combine all search terms for logging.
            all_data = f'{all_data}{i} '
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "shodan", "scanning"])} &a{i}')
            servers = search.search(i)

            for server in servers['matches']:
                # Collect server IP addresses and ports.
                server_list.append(f'{str(server["ip_str"])}:{str(server["port"])}')

        if len(server_list) >= 1:
            # Remove duplicate entries and display the number of servers found.
            server_list = list(set(server_list))
            message_found_ips = str(GetUtilities.get_translated_text(["commands", "shodan", "ipsFound"])).replace('[0]', str(len(server_list))).replace('[1]', all_data[:-1])
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{message_found_ips}')
            log_file = LogManager.create_log_file('shodan')

        else:
            # If no servers are found, display a message.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "shodan", "serversNotFound"])} &f&l(&a{all_data[:-1]}&f&l)')
            return

        for server in server_list:
            server_data = GetMinecraftServerData.get_data(server)

            if server_data is not None:
                # Display and log server data for found servers.
                show_server(server_data)
                log_data = list(server_data.values())
                LogManager.write_log(log_file, 'shodan', log_data)
                servers_found += 1

        if servers_found >= 1:
            # Display the number of Minecraft servers found.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversFound"]).replace("[0]", str(servers_found))}')

        else:
            # Display a message when no Minecraft servers are found.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "serversNotFound"])}')

    except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError, KeyboardInterrupt):
        # Handle JSON decoding errors or keyboard interruptions gracefully.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')

    except shodan.exception.APIError as e:
        if 'Invalid API key' in str(e):
            # Handle invalid API key error.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanInvalidApiKey"])}')

        elif 'Access denied' in str(e):
            # Handle access denied error.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}{GetUtilities.get_translated_text(["shodanApiKeyNoAccess"])}')

        else:
            # Handle other Shodan API connection errors.
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "error"])}&f&lThe connection to the Shodan API could not be established.')
