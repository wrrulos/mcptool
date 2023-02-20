#!/usr/bin/python3

import os

from utils.minecraftserver.CheckServer import check_server
from utils.managers.Settings import SettingsManager
from utils.gets.BotArgument import get_bot_argument
from utils.scanners.QuboScanner import quboscanner
from utils.gets.ScanMethod import get_scan_method
from utils.gets.HostNodes import get_host_nodes
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.alerts.Alerts import alert
from utils.scanners.Nmap import nmap
from datetime import datetime

sm = SettingsManager()
settings = sm.read('settings')


def host_command(hostname, ports, scan_method, bot, proxy=None):
    """
    Command that allows you to scan the nodes of
    the selected hostname

    :param hostname: Hostname
    :param ports: Ports
    :param scan_method: Scan Method
    :param bot: Boolean value that decides whether to send a bot or not
    :param proxy: Proxy socks5
    """

    file = create_file('host')
    logs = LogsManager('host', file)
    timed_out_servers_found = 0
    servers_found = 0
    node_number = 0
    scan_file = ''

    if not hostname.endswith('.json'):
        hostname = f'{hostname}.json'

    try:
        nodes = get_host_nodes(hostname)

        if not nodes:
            paint(f'\n    {language["commands"]["host"]["NODES_NOT_AVAILABLE"]}')
            return
        
        scan_method = get_scan_method(scan_method)
        hostname = hostname.replace('.json', '')
        bot = get_bot_argument(bot)
        logs.create(hostname, ports, scan_method)
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["host"]["FOUND_NODES"].replace("[0]", str(len(nodes))).replace("[1]", hostname.capitalize())}')
                
        for node in nodes:
            date = datetime.now()
            node_number += 1
            scan_file = f'temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'  # Text scan_file 
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["host"]["SCANNING"].replace("[0]", str(node_number)).replace("[1]", hostname.capitalize()).replace("[2]", node)}')

            if scan_method == 'nmap':
                ip_list = nmap(node, ports, scan_file)

            if scan_method == 'quboscanner':
                ip_list = quboscanner(node, ports)

            try:
                os.remove(scan_file)

            except FileNotFoundError:
                pass

            if ip_list == 'CtrlC':
                return

            if len(ip_list) == 0: 
                paint(f'\n    {language["script"]["PREFIX"]}{str(language["commands"]["host"]["NO_PORTS_FOUND"])}')
                continue

            for ip in ip_list:
                check = check_server(ip, bot, proxy, logs)

                if check is None:
                    continue

                if check == 'CtrlC':
                    return

                if check:
                    servers_found += 1

                else:
                    timed_out_servers_found += 1

        if timed_out_servers_found >= 1:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["host"]["FINISHED_SCAN_2"].replace("[0]", hostname).replace("[1]", str(servers_found)).replace("[2]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["host"]["FINISHED_SCAN_1"].replace("[0]", str(hostname)).replace("[1]", str(servers_found))}')

        alert('Alert-0')
    
    except KeyboardInterrupt:
        try:
            os.remove(scan_file)

        except FileNotFoundError:
            pass
        
        return

    
