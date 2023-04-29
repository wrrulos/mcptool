import os

from utils.alerts.Alerts import alert
from utils.checks.Nmap import check_nmap
from utils.color.TextColor import paint
from utils.gets.BotArgument import get_bot_argument
from utils.gets.IPsFromFile import get_ips_from_file
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.gets.ScanFile import get_scan_file
from utils.gets.ScanMethod import get_scan_method
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager
from utils.minecraft.CheckServer import check_server
from utils.scanners.Nmap import nmap
from utils.scanners.QuboScanner import quboscanner


def scan_command(target, ports, scan_method, bot, proxy=None):
    """ 
    It scans the specified ports of an IP address 
    (can also be an IP range) and checks if you 
    have Minecraft servers hosted on its ports.

    Parameters:
        target (str): IP Address
        ports (str): Port range (Examples: 25560-25570)
        scan_method (str): The scanner to use. (For example nmap)
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')
    timed_out_servers_found = 0
    servers_found = 0

    # Gets the value of the scan_method parameter.
    scan_method = get_scan_method(scan_method)

    if scan_method == 'nmap':
        if not check_nmap():
            paint(f'\n    {str(language["commands"]["scan"]["NMAP_NOT_INSTALLED"])}')
            return

    # Gets the value of the bot parameter.
    bot = get_bot_argument(bot) 

    # Gets the name to use for the scan file
    scan_file = get_scan_file()

    # Create a file to save the logs.
    file = create_file('scan')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('scan', file)

    try:
        if target.endswith('.txt'):
            ips_to_scan = get_ips_from_file(target)

            if len(ips_to_scan) == 0:
                paint(f'\n    {language["script"]["PREFIX"]}{str(language["commands"]["scan"]["NO_IPS_FOUND"])}')
                return
            
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["SCANNING_3"].replace("[0]", os.path.basename(target)).replace("[1]", str(len(ips_to_scan)))}')

        elif ',' in target or '*' in target:  # If it is an IP range:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["SCANNING_2"].replace("[0]", target)}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["scan"]["SCANNING_1"].replace("[0]", target)}')
        
        if target.endswith('.txt'):
            ip_list = []

            for ip in ips_to_scan:
                if scan_method == 'nmap':
                    ips = nmap(ip, ports, scan_file)

                if scan_method == 'quboscanner':
                    ips = quboscanner(ip, ports)

                if ips == 'CtrlC':
                    return

                if len(ips) >= 1:
                    for ip in ips:
                        ip_list.append(ip)
        
        else:
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
            paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["SCAN_FINISHED_1"].replace("[0]", str(servers_found))}')

        if settings['SOUNDS']:
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
