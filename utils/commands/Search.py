#!/usr/bin/python3

# This command is in charge of searching for servers 
# with the shodan search engine.

import requests
import shodan
import json

from utils.minecraftserver.CheckServer import check_server
from utils.managers.Settings import SettingsManager
from utils.managers.Logs import LogsManager
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.color.TextColor import paint
from utils.alerts.Alerts import alert

sm = SettingsManager()
settings = sm.read('settings')


def search_command(data):
    """
    Use the Shodan search engine to search for IP addresses that have port 25565 open and then
    check if they are from Minecraft, to finally show it on the screen. 

    :param: Data that will be used to search for servers
    """
    
    file = create_file('search')
    logs = LogsManager('search', file)

    text = ' '.join(data)
    data = text[7:] 
    data = data.split(' --- ')
    servers_found = 0
    timed_out_servers_found = 0
    server_list = []

    try:
        search = shodan.Shodan(settings['SHODAN_TOKEN'])
        all_data = ''
        
        for i in data:
            srvs_found = 0 
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["SCANNING"]} [lgreen]{i}')
            all_data = f'{all_data}{i} '
            servers = search.search(i)

            for server in servers['matches']:
                ip = str(server['ip_str'])
                port = str(server['port'])
                server_list.append(f'{ip}:{port}')
                srvs_found += 1

            if srvs_found >= 1:
                message_found_ips = str(language["commands"]["search"]["IPS_FOUND"]).replace('[0]', str(srvs_found)
                                                                                            ).replace('[1]', i)
                paint(f'\n    {language["script"]["PREFIX"]}{message_found_ips}')

        if len(server_list) == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["SERVERS_NOT_FOUND"]} [lwhite]([lgreen]{all_data[:-1]}[lwhite])')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["CHECKING_SERVERS"]}')
        logs.create(all_data)
        data = ' '.join(data)

        for ip in server_list: 
            check = check_server(ip, None, None, logs)

            if check is None:
                return

            if check:
                servers_found += 1

            else:
                timed_out_servers_found += 1

        if settings['SHOW_TIMED_OUT_SERVERS'] and timed_out_servers_found >= 1:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["FINISHED_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["search"]["FINISHED_1"].replace("[0]", str(servers_found))}')

        alert('Alert-0')

    except KeyboardInterrupt:
        return

    except (json.decoder.JSONDecodeError, requests.exceptions.JSONDecodeError, shodan.exception.APIError):
        return
