import os

from utils.checks.BotArgument import check_bot_argument
from utils.checks.IP import check_ip
from utils.checks.IPRange import check_iprange
from utils.checks.IPPort import check_ip_port
from utils.checks.Language import check_language
from utils.checks.LoopAgument import check_loop_argument
from utils.checks.Port import check_port
from utils.checks.PortRange import check_port_range
from utils.checks.ScanMethod import check_scan_method
from utils.color.TextColor import paint
from utils.checks.ForwardingModeArgument import check_forwardingmode_argument
from utils.gets.Language import language
from utils.minecraft.CheckVersion import check_minecraft_version


def missing_arguments(command, number_of_arguments, arguments):
    """
    Checks if all required arguments exist.

    Parameters:
    command (str): Command name.
    number_of_arguments (int): Number of arguments the command has.
    arguments (list): List of arguments entered by the user.

    Returns:
    bool: True if missing arguments otherwise false.
    """

    for i in range(1, int(number_of_arguments)+1):
        try:
            arguments[i]

        except IndexError:
            paint(f'\n    {language["commands"][command][f"MISSING_ARGUMENT_{str(i)}"]}')
            paint(f'\n    {language["commands"]["USAGE"]}{language["commands"][command]["USAGE"]}')
            return True
        
    return False
        

def check_proxy_argument(number, arguments):
    """ 
    Check if the proxy argument exists and 
    is valid.

    Parameters:
    number (int): Argument number
    arguments (list): List of arguments entered by the user.
    
    Returns:
    bool or None: Returns True if the argument exists and is valid.  \
        False if it exists but is invalid. Returns None if the  \
        argument does not exist.
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
     
    Parameters:
    command (str): Command name
    arguments (list): List of arguments entered by the user.
    
    Returns:
    bool: True if the arguments are valid, False if they are invalid.
    """

    global language

    if command == 'server':
        if missing_arguments(command, 1, arguments):
            return False

    if command == 'player':
        if missing_arguments(command, 1, arguments):
            return False

    if command == 'ipinfo':
        if missing_arguments(command, 1, arguments):
            return False

        if not check_ip(arguments[1]):
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP"]}')
            return False

    if command == 'reverseip':
        if missing_arguments(command, 1, arguments):
            return False

        if not check_ip(arguments[1]):
            paint(f'\n    {language["commands"]["ERROR"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP"]}')
            return False

    if command == 'dnslookup':
        if missing_arguments(command, 1, arguments):
            return False

    if command == 'search':
        if missing_arguments(command, 1, arguments):
            return False
        
    if command == 'websearch':
        if missing_arguments(command, 2, arguments):
            return False

        if not check_bot_argument(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
    if command == 'aternos':
        if missing_arguments(command, 2, arguments):
            return False
        
        try:
            if int(arguments[1]) <= 0:
                paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PAGE_ARGUMENT"]}')
                return False
            
        except ValueError:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PAGE_ARGUMENT"]}')
            return False
            
        if not check_bot_argument(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(3, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'scan':
        if missing_arguments(command, 4, arguments):
            return False

        if str(arguments[1]).endswith('.txt') or '/' in arguments[1] or '\\' in arguments[1]:
            if not os.path.exists(arguments[1]):
                paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FILE"].replace("[0]", arguments[1])}')
                return False

        else:
            if '-' in arguments[1] or '*' in arguments[1]:
                if not check_iprange(arguments[1]):
                    paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP_RANGE"]}')
                    return False

            else:
                if not check_ip(arguments[1]):
                    paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_IP"]}')
                    return False

        if ',' in arguments[2] or '-' in arguments[2]:
            if not check_port_range(arguments[2]):
                paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PORTS"]}')
                return False

        else:
            if not check_port(arguments[2]):
                paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PORTS"]}')
                return False

        if not check_scan_method(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SCAN_METHOD"]}')
            return False

        if not check_bot_argument(arguments[4]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'checker':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not os.path.exists(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FILE"].replace("[0]", arguments[1])}')
            return False
        
        if not check_bot_argument(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_BOT_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(3, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'listening':
        if missing_arguments(command, 1, arguments):
            return False

    if command == 'playerlogs':
        if missing_arguments(command, 1, arguments):
            return False
        
    if command == 'bungee':
        if missing_arguments(command, 1, arguments):
            return False
        
    if command == 'velocity':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not check_forwardingmode_argument(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FORWARDING_MODE"]}')
            return False

    if command == 'fakeproxy':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not check_forwardingmode_argument(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FORWARDING_MODE"]}')
            return False
        
    if command == 'connect':
        if missing_arguments(command, 3, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False

        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_VERSION"]}')
            return False

    if command == 'rconnect':
        if missing_arguments(command, 2, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False

    if command == 'rcon':
        if missing_arguments(command, 2, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False

        if not os.path.exists(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FILE"].replace("[0]", arguments[2])}')
            return False
    
    if command == 'authme':
        if missing_arguments(command, 4, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_VERSION"]}')
            return False

        if not os.path.exists(arguments[4]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FILE"].replace("[0]", arguments[2])}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'kick':
        if missing_arguments(command, 4, arguments):
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_VERSION"]}')
            return False

        if not check_loop_argument(arguments[4]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_LOOP_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'kickall':
        if missing_arguments(command, 3, arguments):
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[2]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_VERSION"]}')
            return False
        
        if not check_loop_argument(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_LOOP_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(4, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'sendcmd':
        if missing_arguments(command, 5, arguments):
            return False
                
        if not check_ip_port(arguments[1]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return False
        
        if not check_minecraft_version(arguments[3]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_VERSION"]}')
            return False
        
        if not os.path.exists(arguments[4]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_FILE"].replace("[0]", arguments[4])}')
            return False

        if not check_loop_argument(arguments[5]):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_LOOP_ARGUMENT"]}')
            return False
        
        if check_proxy_argument(6, arguments) is False:
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_PROXY"]}')
            return False
        
    if command == 'language':
        if missing_arguments(command, 1, arguments):
            return False
        
        if not check_language(arguments[1].lower()):
            paint(f'\n    {language["commands"]["INVALID_ARGUMENTS"]["INVALID_LANGUAGE"]}')
            paint(f'\n    {language["commands"]["language"]["LANGUAGE_LIST"]}')
            return False

    return True