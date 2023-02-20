#!/usr/bin/python3

import os

from utils.minecraftserver.CheckServer import check_server
from utils.gets.BotArgument import get_bot_argument
from utils.managers.Settings import SettingsManager
from utils.scanners.QuboScanner import quboscanner
from utils.gets.ScanMethod import get_scan_method
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.alerts.Alerts import alert
from utils.scanners.Nmap import nmap
from datetime import datetime

sm = SettingsManager()
settings = sm.read('settings')


def scan_command(target, ports, scan_method, bot, proxy=None):
    """ 
    Command that allows you to scan a range 
    of ports to an IP address. 

    :param target: IP adress
    :param ports: Ports
    :param scan_method: Scan Method
    :param bot: Boolean value that decides whether to send a bot or not
    :param proxy: Proxy socks5
    """
    
    file = create_file('scan')
    logs = LogsManager('scan', file)
    date = datetime.now()
    timed_out_servers_found = 0
    servers_found = 0
    scan_file = f'temp_scan_{str(date.day)}-{str(date.month)}-{str(date.year)}_{str(date.hour)}.{str(date.minute)}.{str(date.second)}.txt'  # Text scan_file 

    try:
        scan_method = get_scan_method(scan_method)  # Get the scan method
        bot = get_bot_argument(bot)  # Gets the bot argument

        if ',' in target or '*' in target:  # If it is an IP range:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["SCANNING_2"].replace("[0]", target)}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["SCANNING_1"].replace("[0]", target)}')
        
        if scan_method == 'nmap':
            ip_list = nmap(target, ports, scan_file)

        if scan_method == 'quboscanner':
            ip_list = quboscanner(target, ports)

        if ip_list == 'CtrlC':
            return

        if len(ip_list) == 0: 
            paint(f'\n    {language["script"]["PREFIX"]}{str(language["commands"]["scan"]["NO_PORTS_FOUND"])}')
            return

        logs.create(target, ports, scan_method)
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["CHECKING_PORTS"].replace("[0]", str(len(ip_list)))}')

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
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["FINISHED_SCAN_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["FINISHED_SCAN_1"].replace("[0]", str(servers_found))}')

        alert('Alert-0')
        os.remove(scan_file)
            
    except KeyboardInterrupt:
        try:
            os.remove(scan_file)

        except FileNotFoundError:
            pass

        return

    except FileNotFoundError:
        return