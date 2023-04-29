import os
import re
import subprocess

from utils.checks.Encoding import check_encoding
from utils.checks.Folder import check_folders
from utils.checks.IPPort import check_ip_port
from utils.managers.Settings import SettingsManager


def quboscanner(target, ports):
    """ 
    Scan the specified target using QuboScanner

    Parameters:
        target (str): IP address
        ports (str): Ports Range
    
    Returns:
        list: IP list
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    try:
        ip_list = []
        scan_file = None

        check_folders('utils/scanners/quboscanner/outputs')
        file_list = os.listdir('utils/scanners/quboscanner/outputs')  # Save current quboscanner outputs to a list
        command = settings['QUBO_COMMAND'].replace('[0]', target
                                         ).replace('[1]', ports
                                         ).replace('[2]', settings["QUBO_THREADS"]
                                         ).replace('[3]', settings["QUBO_TIMEOUT"])

        subprocess.run(f'cd utils/scanners/quboscanner && {command}', shell=True)
        new_file_list = os.listdir('utils/scanners/quboscanner/outputs')  # Save current quboscanner outputs back to another list

        for file in new_file_list:
            if file not in file_list:
                scan_file = f'utils/scanners/quboscanner/outputs/{file}'
                break
        
        if scan_file is None:
            return ip_list

        with open(scan_file, 'r', encoding=check_encoding(scan_file)) as f:
            for line in f:
                ips = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}', line)

                for ip in ips:
                    if check_ip_port(ip):
                        ip_list.append(ip)

        return ip_list
    
    except KeyboardInterrupt:
        if scan_file is not None:
            try:
                os.remove(scan_file)

            except FileNotFoundError:
                pass

        return 'CtrlC'


    
