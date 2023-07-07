import os


from utils.sounds.play_sound import play_sound
from utils.checks.check_nmap import check_nmap
from utils.checks.check_masscan import check_masscan
from utils.color.text_color import paint
from utils.gets.get_bot_argument import get_bot_argument
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.gets.get_scan_method import get_scan_method
from utils.managers.logs_manager import LogsManager
from utils.managers.config_manager import config_manager
from utils.scanners.scan import scan
from utils.gets.get_spaces import get_spaces


def scan_command(target, ports, scan_method, bot, proxy_file=None):
    """ 
    It scans the specified ports of an IP address 
    (can also be an IP range) and checks if you 
    have Minecraft servers hosted on its ports.

    Args:
        target (str): IP Address
        ports (str): Port range (Examples: 25560-25570)
        scan_method (str): The scanner to use. (For example nmap)
        bot (bool): Indicates if a bot will be sent to verify login to the server.
        proxy_file (str): Optional proxy file to use for the bot.
    """

    ips_to_scan = []
    output = ''

    # Gets the value of the scan_method parameter.
    scan_method = get_scan_method(scan_method)

    # If the user chooses nmap, check if they have nmap installed.
    if scan_method == 'nmap':
        if not check_nmap():
            paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["scan"]["nmapNotInstalled"])}')
            return

    if scan_method == 'masscan':
        if not check_masscan():
            paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["scan"]["masscanNotInstalled"])}')
            return

    # Gets the value of the bot parameter.
    bot = get_bot_argument(bot)

    # Create a file to save the logs.
    file = create_file('scan')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('scan', file)

    servers_found = 0
    timed_out_servers_found = 0

    try:
        if target.endswith('.txt'):
            with open(target, 'r') as f:
                for line in f:
                    line = line.strip()

                    if line:
                        ips_to_scan.append(line)

            if len(ips_to_scan) == 0:
                paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{str(language_manager.language["commands"]["scan"]["noIpsFound"])}')
                return
            
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["scan"]["scanning3"].replace("[0]", os.path.basename(target)).replace("[1]", str(len(ips_to_scan)))}')

        elif ',' in target or '*' in target:  # If it is an IP range:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["scan"]["scanning2"].replace("[0]", target)}')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["scan"]["scanning1"].replace("[0]", target)}')

        if target.endswith('.txt'):
            for target in ips_to_scan:
                output = scan(target, ports, scan_method, bot, proxy_file, logs)

                if output is not None:
                    if output == 'CtrlC':
                        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
                        return

                    servers_found += int(output[0])
                    timed_out_servers_found += int(output[1])

                else:
                    return
        else:
            output = scan(target, ports, scan_method, bot, proxy_file, logs)

            if output is not None:
                if output == 'CtrlC':
                    paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
                    return

                servers_found = int(output[0])
                timed_out_servers_found = int(output[1])

            else:
                return

        if servers_found == 0:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{str(language_manager.language["commands"]["scan"]["noPortsFound"])}')
            return

        logs.create(target, ports, scan_method)

        if timed_out_servers_found >= 1:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["scanFinished2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["scanFinished1"].replace("[0]", str(servers_found))}')

        if config_manager.config['sounds']:
            play_sound('sound1')

    except (KeyboardInterrupt, FileNotFoundError):
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
