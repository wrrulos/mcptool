import subprocess
import os
import re

from utils.color.text_color import paint
from utils.gets.get_scan_command import get_scan_command
from utils.checks.check_termux import check_termux
from utils.minecraft.check_server import check_server
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def scan(target, ports, scan_method, bot=False, proxy_file=None, logs=None):
    """
    Perform scanning of the specified target using Quboscanner.

    Args:
        target (str): Target to scan (It can be an IP or an IP range).
        ports (str): Ports range.
        scan_method (str): Scan method.
        bot (bool):
        proxy_file (str):
        logs (str):

    Returns:
        Tuple[int, int]: A tuple containing the number of servers found and the number of servers that timed out.
    """

    text_to_search = ''
    pattern = ''
    invalid_ip_text = ''
    invalid_ports_text = ''
    servers_found = 0
    timed_out_servers_found = 0

    # Gets the command to scan.
    command = get_scan_command(scan_method, target, ports)

    try:
        if os.name != 'nt' and scan_method != 'new_quboscanner' and scan_method != 'old_quboscanner' and not check_termux():
            command = f'sudo {command}'

        # Create a subprocess for running the Nmap command.
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        if scan_method == 'nmap' or scan_method == 'masscan':
            text_to_search = 'Discovered open port'
            pattern = r'open port (\d+)/\w+ on (\d+\.\d+\.\d+\.\d+)'

        if scan_method == 'nmap':
            invalid_ip_text = ['Failed to resolve "']
            invalid_ports_text = ['Your port specifications are illegal.', 'Your port range']

        if scan_method == 'masscan':
            invalid_ip_text = ['ERROR: bad IP address/range:']
            invalid_ports_text = []

        if scan_method == 'old_quboscanner' or scan_method == 'new_quboscanner':
            text_to_search = ')('
            pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+\b'
            invalid_ip_text = ['Invalid IP range.']
            invalid_ports_text = ['port is out of range', 'For input string:']

        # Iterate over the output lines of the process.
        for line in process.stdout:
            output_line = line.decode('latin-1').strip()

            # In the event that the text appears indicating that the ip entered is invalid.
            for text in invalid_ip_text:
                if text in output_line:
                    paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidIpRange"].replace("[0]", target)}')
                    process.terminate()
                    return None

            # In the event that the text appears indicating that the ports entered is invalid.
            for text in invalid_ports_text:
                if text in output_line:
                    paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidPorts"].replace("[0]", ports)}')
                    process.terminate()
                    return None

            # When it finds an open port.
            if text_to_search in output_line:
                match = re.search(pattern, output_line)

                if match:
                    if scan_method == 'nmap' or scan_method == 'masscan':
                        server = f'{match.group(2)}:{match.group(1)}'

                    else:
                        server = match.group(0)

                    # Check the status of the server.
                    check = check_server(server, bot, proxy_file, logs)

                    if check is not None:
                        if check == 'CtrlC':
                            process.terminate()
                            return [servers_found, timed_out_servers_found]

                        elif check:
                            servers_found += 1

                        else:
                            timed_out_servers_found += 1

        # Wait for the process to finish
        process.wait()
        return [servers_found, timed_out_servers_found]

    except (KeyboardInterrupt, ValueError):
        try:
            process.terminate()

        except UnboundLocalError:
            pass

        return 'CtrlC'