import json
import requests
import shodan

from utils.alerts.Alerts import alert
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager
from utils.minecraft.CheckServer import check_server


def search_command(*data):
    """
    Use the Shodan search engine to search for IP addresses 
    that have port 25565 open and then check if they are 
    from Minecraft, to finally show it on the screen. 

    Parameters:
    data (str): Data that will be used to search for servers.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    servers_found = 0
    timed_out_servers_found = 0
    server_list = []

    if settings['SHODAN_API_KEY'] == '':
        paint(f'\n    {language["commands"]["ERROR"]}{language["other_messages"]["SHODAN_INVALID_API_KEY"]}')
        return
    
    try:
        api = shodan.Shodan(settings['SHODAN_API_KEY'])
        _ = api.info()

    except shodan.exception.APIError:
        paint(f'\n    {language["commands"]["ERROR"]}{language["other_messages"]["SHODAN_INVALID_API_KEY"]}')
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
        search = shodan.Shodan(settings['SHODAN_API_KEY'])
        all_data = ''
        
        # Separates the data entered by the user.
        for i in data:
            srvs_found = 0 
            all_data = f'{all_data}{i} '
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["SCANNING"]} &a{i}')
            servers = search.search(i)

            for server in servers['matches']:
                server_list.append(f'{str(server["ip_str"])}:{str(server["port"])}')
                srvs_found += 1

            if srvs_found >= 1:
                message_found_ips = str(language["commands"]["search"]["IPS_FOUND"]).replace('[0]', str(srvs_found)
                                                                                   ).replace('[1]', i)
                paint(f'\n    {language["script"]["PREFIX"]}{message_found_ips}')

        if len(server_list) == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["SERVERS_NOT_FOUND"]} &f&l(&a{all_data[:-1]}&f&l)')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["CHECKING_SERVERS"]}')
        logs.create(all_data)

        for ip in server_list: 
            check = check_server(ip, None, None, logs)

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

    except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError, shodan.exception.APIError, KeyboardInterrupt):
        return
