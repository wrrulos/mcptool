import time
import re

from utils.checks.check_folder import check_folders
from utils.writefile.write_file import WriteFile
from utils.mccolor.mc_remove import mcremove

base = '''
################
# MCPTool Logs #
################

[>] General information

[#] Command: [0]
[#] Time and date: [1]

[>] Command information: 
[2]'''

save_bedrock_server = '''
[IP] [1] ([0])
[MOTD] [2]
[Version] [3]
[Protocol] [4]
[Players] [5]/[6]
[Map] [7]
[Gamemode] [8]
'''

save_java_server = '''
[IP] [1] ([0])
[MOTD] [2]
[Version] [3]
[Protocol] [4]
[Players] [5]/[6]
'''

save_server_with_bot = f'[Checker] [OUTPUT]\n'

save_timed_out_server = '''
[TimedOut] [0]
'''

save_player = '[Player] [0]\n'
save_player_log = '[0] [Player] [1]\n'


class LogsManager:
    def __init__(self, command, file):
        self.command = command
        self.file = file

    def create(self, *data):
        check_folders('logs', f'logs/{self.command}')

        if self.command == 'search':
            information = f'[#] Data: {data[0]}\n'

        if self.command == 'websearch':
            information = f'[#] Tag: {data[0]}\n'

        if self.command == 'scan':
            information = f'[#] Target: {data[0]}\n[#] Ports: {data[1]}\n[#] Scanning Method: {data[2]}\n'

        if self.command == 'host':
            information = f'[#] Host: {data[0]}\n[#] Ports: {data[1]}\n[#] Scanning Method: {data[2]}\n'

        if self.command == 'aternos':
            information = f'[#] Pages: {data[0]}\n'

        if self.command == 'checker':
            information = f'[#] File: {data[0]}\n'

        if self.command == 'listening' or self.command == 'playerlogs':
            information = f'[#] Server: {data[0]}\n\n'

        if self.command == 'fakeproxy':
            information = f'[#] Server: {data[0]}\n[#] Forwarding mode: {data[1]}\n\n[>] Captured data:\n\n'

        if self.command == 'rcon':
            information = f'[#] Server: {data[0]}\n[#] Password File: {data[1]}\n\n'
            
        logs = base.replace('[0]', self.command
                    ).replace('[1]', time.ctime()
                    ).replace('[2]', information)

        WriteFile(self.file, True, 'w+', logs)

    def write(self, data_type, data, output=None):
        if data_type == 'save_server':
            if data[0] == 'Java':
                information = save_java_server

            else:
                information = save_bedrock_server

            for num, i in enumerate(data):
                if i is None:
                    continue

                i = self._clear_data(str(i))
                information = information.replace(f'[{str(num)}]', str(i))

            if output is not None:
                information = f'{information}{save_server_with_bot.replace(f"[OUTPUT]", str(output))}'

        if data_type == 'save_timed_out_server':
            information = save_timed_out_server.replace('[0]', data)

        if data_type == 'save_player':
            information = save_player.replace('[0]', data)
            information = information.replace('&f&l', ''
                                    ).replace('&a', 'ONLINE: '
                                    ).replace('&c', 'OFFLINE: '
                                    ).replace('&5', 'CUSTOMIZED: ')
            
        if data_type == 'save_player_log':
            information = save_player_log.replace('[0]', data[0]).replace("[1]", data[1])
            information = information.replace('&f&l', ''
                                    ).replace('&a', 'ONLINE: '
                                    ).replace('&c', 'OFFLINE: '
                                    ).replace('&5', 'CUSTOMIZED: ')

        if data_type == 'save_data_from_fakesrv':
            information = data

        if data_type == 'save_rcon_password':
            information = f'[!] RCON Password: {data}'

        WriteFile(self.file, False, 'a', information)

    def _clear_data(self, data):
        data = mcremove(data)
        data = data.replace('\n', '')
        data = re.sub(' +', ' ', data)
        return data
