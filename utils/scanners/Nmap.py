import os
import re
import subprocess

from utils.checks.Encoding import check_encoding
from utils.managers.Settings import SettingsManager


def nmap(target, ports, file):
    """ 
    Scan the specified target using Nmap 

    Parameters:
    target (str): IP address
    ports (str): Ports Range
    file (str): Scan file
    
    Returns:
    list: IP list
    """
    
    sm = SettingsManager()
    settings = sm.read('settings')

    try:
        ip_list = []
        command = settings['NMAP_COMMAND'].replace('[0]', ports
                                         ).replace('[1]', file
                                         ).replace('[2]', target)

        subprocess.run(command, shell=True)

        with open(file, 'r', encoding=check_encoding(file)) as f:
            for line in f:
                ip = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)  # Search for an ip address in the line.
                ip = ' '.join(ip)
                ip = ip.replace('(', '').replace(')', '')

                port = re.findall('\d{1,5}\/tcp open', line)  # Search for an open port in the line.
                port = ' '.join(port)
            
                if len(port) == 0:  # If it doesn't find an open port, it tries to search for a filtered one.
                    if settings['SHOW_NMAP_FILTERED_PORTS']:
                        port = re.findall('\d{1,5}\/tcp filtered', line)
                        port = ' '.join(port)

                if '.' in ip:
                    current_ip = ip

                if 'tcp' in port:
                    port = port.replace('/tcp open', '').replace('/tcp filtered', '')
                    current_ip_backup = current_ip

                    try:
                        current_ip = current_ip.split(' ')
                        current_ip = current_ip[1]

                    except IndexError:
                        current_ip = current_ip_backup

                    ip_list.append(f'{current_ip}:{port}')

            return ip_list
    
    except KeyboardInterrupt:
        try:
            os.remove(file)

        except FileNotFoundError:
            pass

    return 'CtrlC'
