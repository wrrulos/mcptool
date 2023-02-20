#!/usr/bin/python3

import os

from utils.minecraftserver.CheckVersion import check_minecraft_version
from utils.checks.LoopAgument import check_loop_argument
from utils.checks.BotArgument import check_bot_argument
from utils.checks.ScanMethod import check_scan_method
from utils.checks.PortRange import check_port_range
from utils.checks.Language import check_language
from utils.checks.IPRange import check_iprange
from utils.checks.IPPort import check_ip_port
from utils.checks.Port import check_port
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.checks.IP import check_ip


def missing_argument(number, arguments):
    """ 
    Check if the argument exists 
    
    :param number: Argument number
    :param arguments: All Arguments
    :return: Returns True if the argument is missing, false if it exists
    """

    try:
        arguments[number]
        return False

    except IndexError:
        return True
    

def check_proxy_argument(number, arguments):
    """ 
    Check if the proxy argument exists and is valid
    
    :param number: Argument number
    :param arguments: All Arguments
    :return: True if the argument exists and is valid, False if it exists but is invalid, None if it does not exist
    """

    try:
        arguments[number]

        if check_ip_port(arguments[number]):
            return True

        return False
    
    except IndexError:
        return None
    

def check_command_arguments(command, arguments):
    """ 
    Checks if the command arguments entered by 
    the user are valid.
     
    :param command: Command name
    :param arguments: All Arguments
    :return: True if the arguments are valid, False if they are invalid.
    """

    global language

    if command == 'server':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["server"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["server"]["USAGE"]}')
            return False

    if command == 'player':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["player"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["player"]["USAGE"]}')
            return False

    if command == 'ipinfo':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["ipinfo"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["ipinfo"]["USAGE"]}')
            return False

        if not check_ip(arguments[1]):
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["ipinfo"]["INVALID_IP"]}')
            return False

    if command == 'dnslookup':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["dnslookup"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["dnslookup"]["USAGE"]}')
            return False

    if command == 'search':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["search"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["search"]["USAGE"]}')
            return False
        
    if command == 'scan':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["scan"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["scan"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["scan"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["scan"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["scan"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["scan"]["USAGE"]}')
            return False

        if missing_argument(4, arguments):
            paint(f'\n    {language["commands"]["scan"]["MISSING_ARGUMENT_4"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["scan"]["USAGE"]}')
            return False

        if str(arguments[1]).endswith('.txt'):
            if not os.path.exists(arguments[1]):
                paint(f'\n    {language["commands"]["scan"]["FILE_NOT_FOUND"].replace("[0]", arguments[1])}')
                return False

        else:
            if '-' in arguments[1] or '*' in arguments[1]:
                if not check_iprange(arguments[1]):
                    paint(f'\n    {language["commands"]["scan"]["INVALID_IP_RANGE"]}')
                    return False

            else:
                if not check_ip(arguments[1]):
                    paint(f'\n    {language["commands"]["scan"]["INVALID_IP"]}')
                    return False

        if ',' in arguments[2] or '-' in arguments[2]:
            if not check_port_range(arguments[2]):
                paint(f'\n    {language["commands"]["scan"]["INVALID_PORTS"]}')
                return False

        else:
            if not check_port(arguments[2]):
                paint(f'\n    {language["commands"]["scan"]["INVALID_PORTS"]}')
                return False

        if not check_scan_method(arguments[3]):
            paint(f'\n    {language["commands"]["scan"]["INVALID_SCAN_METHOD"]}')
            return False

        if not check_bot_argument(arguments[4]):
            paint(f'\n    {language["commands"]["scan"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["scan"]["INVALID_PROXY"]}')
            return False
        
    elif command == 'host':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["host"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["host"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["host"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["host"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["host"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["host"]["USAGE"]}')
            return False

        if missing_argument(4, arguments):
            paint(f'\n    {language["commands"]["host"]["MISSING_ARGUMENT_4"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["host"]["USAGE"]}')
            return False
        
        if not str(arguments[1]).endswith('.json'):
            arguments[1] = f'{str(arguments[1])}.json'

        if not os.path.exists(f'utils/hostnames/{arguments[1]}'):
            paint(f'\n    {language["commands"]["host"]["INVALID_HOSTNAME"]}')
            return False

        if ',' in arguments[2] or '-' in arguments[2]:
            if not check_port_range(arguments[2]):
                paint(f'\n    {language["commands"]["host"]["INVALID_PORTS"]}')
                return False

        else:
            if not check_port(arguments[2]):
                paint(f'\n    {language["commands"]["host"]["INVALID_PORTS"]}')
                return False

        if not check_scan_method(arguments[3]):
            paint(f'\n    {language["commands"]["host"]["INVALID_SCAN_METHOD"]}')
            return False

        if not check_bot_argument(arguments[4]):
            paint(f'\n    {language["commands"]["host"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["host"]["INVALID_PROXY"]}')
            return False
        
    if command == 'checker':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["checker"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["checker"]["USAGE"]}')
            return False
        
        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["checker"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["checker"]["USAGE"]}')
            return False
        
        if not os.path.exists(arguments[1]):
            paint(f'\n    {language["commands"]["checker"]["FILE_NOT_FOUND"].replace("[0]", arguments[1])}')
            return False
        
        if not check_bot_argument(arguments[2]):
            paint(f'\n    {language["commands"]["checker"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(3, arguments) is False:
            paint(f'\n    {language["commands"]["checker"]["INVALID_PROXY"]}')
            return False
        
    if command == 'listening':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["listening"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["listening"]["USAGE"]}')
            return False

    if command == 'bungee':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["bungee"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["bungee"]["USAGE"]}')
            return False

    if command == 'poisoning':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["poisoning"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["poisoning"]["USAGE"]}')
            return False
        
    if command == 'connect':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["connect"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["connect"]["USAGE"]}')
            return False
        
        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["connect"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["connect"]["USAGE"]}')
            return False
        
        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["connect"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["connect"]["USAGE"]}')
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["connect"]["INVALID_SERVER"]}')
            return False

        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["connect"]["INVALID_VERSION"]}')
            return False

    if command == 'rconnect':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["rconnect"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["rconnect"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["rconnect"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["rconnect"]["USAGE"]}')
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["rconnect"]["INVALID_SERVER"]}')
            return False

    if command == 'rcon':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["rcon"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["rcon"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["rcon"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["rcon"]["USAGE"]}')
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["rcon"]["INVALID_SERVER"]}')
            return False

        if not os.path.exists(arguments[2]):
            paint(f'\n    {language["commands"]["rcon"]["FILE_NOT_FOUND"].replace("[0]", arguments[2])}')
            return False
    
    if command == 'authme':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["authme"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["authme"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["authme"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["authme"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["authme"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["authme"]["USAGE"]}')
            return False

        if missing_argument(4, arguments):
            paint(f'\n    {language["commands"]["authme"]["MISSING_ARGUMENT_4"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["authme"]["USAGE"]}')
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["authme"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["authme"]["INVALID_VERSION"]}')
            return False

        if not os.path.exists(arguments[4]):
            paint(f'\n    {language["commands"]["authme"]["FILE_NOT_FOUND"].replace("[0]", arguments[2])}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["authme"]["INVALID_PROXY"]}')
            return False
        
    if command == 'kick':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["kick"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kick"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["kick"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kick"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["kick"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kick"]["USAGE"]}')
            return False
        
        if missing_argument(4, arguments):
            paint(f'\n    {language["commands"]["kick"]["MISSING_ARGUMENT_4"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kick"]["USAGE"]}')
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["kick"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["kick"]["INVALID_VERSION"]}')
            return False

        if not check_loop_argument(arguments[4]):
            paint(f'\n    {language["commands"]["kick"]["INVALID_LOOP_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["kick"]["INVALID_PROXY"]}')
            return False
        
    if command == 'kickall':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["kickall"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kickall"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["kickall"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kickall"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["kickall"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["kickall"]["USAGE"]}')
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["kickall"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[2]):
            paint(f'\n    {language["commands"]["kickall"]["INVALID_VERSION"]}')
            return False
        
        if not check_loop_argument(arguments[3]):
            paint(f'\n    {language["commands"]["kickall"]["INVALID_LOOP_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(4, arguments) is False:
            paint(f'\n    {language["commands"]["kickall"]["INVALID_PROXY"]}')
            return False
        
    if command == 'sendcmd':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["sendcommand"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["sendcommand"]["USAGE"]}')
            return False

        if missing_argument(2, arguments):
            paint(f'\n    {language["commands"]["sendcommand"]["MISSING_ARGUMENT_2"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["sendcommand"]["USAGE"]}')
            return False

        if missing_argument(3, arguments):
            paint(f'\n    {language["commands"]["sendcommand"]["MISSING_ARGUMENT_3"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["sendcommand"]["USAGE"]}')
            return False

        if missing_argument(4, arguments):
            paint(f'\n    {language["commands"]["sendcommand"]["MISSING_ARGUMENT_4"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["sendcommand"]["USAGE"]}')
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["sendcommand"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["sendcommand"]["INVALID_VERSION"]}')
            return False
        
        if not os.path.exists(arguments[4]):
            paint(f'\n    {language["commands"]["sendcommand"]["FILE_NOT_FOUND"].replace("[0]", arguments[2])}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["sendcommand"]["INVALID_PROXY"]}')
            return False
        
    if command == 'language':
        if missing_argument(1, arguments):
            paint(f'\n    {language["commands"]["language"]["MISSING_ARGUMENT_1"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"]["language"]["USAGE"]}')
            return False
        
        if not check_language(arguments[1]):
            paint(f'\n    {language["commands"]["language"]["INVALID_LANGUAGE"]}')
            return False

    return True