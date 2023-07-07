import os

from utils.checks.check_bot_argument import check_bot_argument
from utils.checks.check_ip import check_ip
from utils.checks.check_ip_port import check_ip_port
from utils.checks.check_language import check_language
from utils.checks.check_loop_argument import check_loop_argument
from utils.checks.check_scan_method import check_scan_method
from utils.color.text_color import paint
from utils.checks.check_forwarding_mode_argument import check_forwardingmode_argument
from utils.managers.language_manager import language_manager
from utils.gets.get_spaces import get_spaces


def missing_arguments(command, number_of_arguments, arguments):
    """
    Checks if all required arguments exist.

    Args:
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
            paint(f'\n{get_spaces()}{language_manager.language["commands"][command][f"missingArgument{str(i)}"]}')
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["usage"]}{language_manager.language["commands"][command]["usage"]}')
            return True
        
    return False
        

def check_proxy_argument(number, arguments):
    """ 
    Check if the proxy argument exists and 
    is valid.

    Args:
        number (int): Argument number
        arguments (list): List of arguments entered by the user.

    Returns:
        bool or None: Returns True if the argument exists and is valid.  \
            False if it exists but is invalid. Returns None if the  \
            argument does not exist.
    """
    
    try:
        _ = arguments[number]

        if os.path.exists(arguments[number]):
            return True

        return False
    
    except IndexError:
        return None
    

def check_command_arguments(command, arguments):
    """ 
    Checks if the command arguments entered by
    the user are valid.
     
    Args:
    command (str): Command name
    arguments (list): List of arguments entered by the user.
    
    Returns:
    bool: True if the arguments are valid, False if they are invalid.
    """

    valid_languages = os.listdir('config/lang/')
    valid_languages = ' '.join(valid_languages)
    valid_languages = str(valid_languages).replace('.json', '')
    valid_languages = valid_languages.replace(' ', ', ')

    commands = {
        '00': 'help',
        '01': 'server',
        '02': 'player',
        '03': 'ipinfo',
        '04': 'reverseip',
        '05': 'dnslookup',
        '06': 'search',
        '07': 'websearch',
        '08': 'aternos',
        '09': 'scan',
        '10': 'subdomains',
        '11': 'checker',
        '12': 'listening',
        '13': 'playerlogs',
        '14': 'bungee',
        '15': 'velocity',
        '16': 'fakeproxy',
        '17': 'connect',
        '18': 'rcon',
        '19': 'rconbrute',
        '20': 'login',
        '21': 'pinlogin',
        '22': 'kick',
        '23': 'kickall',
        '24': 'sendcmd',
        '25': 'config',
        '26': 'language',
        '27': 'discord'
    }

    if len(command) == 2:
        command = commands.get(command, command)

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
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["commands"]["invalidArguments"]["invalidIP"]}')
            return False

    if command == 'reverseip':
        if missing_arguments(command, 1, arguments):
            return False

        if not check_ip(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["error"]}{language_manager.language["commands"]["invalidArguments"]["invalidIP"]}')
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
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidBotArgument"]}')
            return False
        
    if command == 'aternos':
        if missing_arguments(command, 2, arguments):
            return False
        
        try:
            if int(arguments[1]) <= 0:
                paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidPageArgument"]}')
                return False
            
        except ValueError:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidPageArgument"]}')
            return False
            
        if not check_bot_argument(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidBotArgument"]}')
            return False
        
        if check_proxy_argument(3, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'scan':
        if missing_arguments(command, 4, arguments):
            return False

        if arguments[3] != 'masscan' and arguments[3] != '2':
            if str(arguments[1]).endswith('.txt') or '/' in arguments[1] or '\\' in arguments[1]:
                if not os.path.exists(arguments[1]):
                    paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[1])}')
                    return False

        if not check_scan_method(arguments[3]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidScanMethod"]}')
            return False

        if not check_bot_argument(arguments[4]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidBotArgument"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'subdomains':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not os.path.exists(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[2])}')
            return False
        
    if command == 'checker':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not os.path.exists(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[1])}')
            return False
        
        if not check_bot_argument(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidBotArgument"]}')
            return False
        
        if check_proxy_argument(3, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'listening':
        if missing_arguments(command, 1, arguments):
            return False

    if command == 'playerlogs':
        if missing_arguments(command, 1, arguments):
            return False
        
    if command == 'waterfall':
        if missing_arguments(command, 1, arguments):
            return False
        
    if command == 'velocity':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not check_forwardingmode_argument(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidForwardingMode"]}')
            return False

    if command == 'fakeproxy':
        if missing_arguments(command, 2, arguments):
            return False
        
        if not check_forwardingmode_argument(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidForwardingMode"]}')
            return False
        
    if command == 'connect':
        if missing_arguments(command, 3, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False
        
        if check_proxy_argument(4, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False

    if command == 'rcon':
        if missing_arguments(command, 2, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

    if command == 'rconbrute':
        if missing_arguments(command, 2, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

        if not os.path.exists(arguments[2]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[2])}')
            return False
    
    if command == 'login':
        if missing_arguments(command, 4, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

        if not os.path.exists(arguments[4]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[4])}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False

    if command == 'pinlogin':
        if missing_arguments(command, 4, arguments):
            return False

        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

        if not os.path.exists(arguments[4]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[4])}')
            return False

        if check_proxy_argument(5, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False

    if command == 'kick':
        if missing_arguments(command, 4, arguments):
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

        if not check_loop_argument(arguments[4]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidLoopArgument"]}')
            return False
        
        if check_proxy_argument(5, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'kickall':
        if missing_arguments(command, 3, arguments):
            return False
        
        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False

        if not check_loop_argument(arguments[3]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidLoopArgument"]}')
            return False
        
        if check_proxy_argument(4, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'sendcmd':
        if missing_arguments(command, 5, arguments):
            return False
                
        if not check_ip_port(arguments[1]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return False
        
        if not os.path.exists(arguments[4]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidFile"].replace("[0]", arguments[4])}')
            return False

        if not check_loop_argument(arguments[5]):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidLoopArgument"]}')
            return False
        
        if check_proxy_argument(6, arguments) is False:
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidProxyFile"]}')
            return False
        
    if command == 'language':
        if missing_arguments(command, 1, arguments):
            return False
        
        if not check_language(arguments[1].lower()):
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["invalidArguments"]["invalidLanguage"]}')
            paint(f'\n{get_spaces()}{language_manager.language["commands"]["language"]["languageList"].replace("[0]", str(valid_languages))}')
            return False

    if command == 'config':
        if missing_arguments(command, 1, arguments):
            return False

    return True
