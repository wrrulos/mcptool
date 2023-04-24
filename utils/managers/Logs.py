import time

from utils.checks.Folder import check_folders
from utils.writefile.WriteFile import WriteFile

base = '''
################
# MCPTool Logs #
################

[>] General information

[#] Command: [0]
[#] Time and date: [1]

[>] Command information: 
[2]'''

save_server = '''
[IP] [0]
[MOTD] [1]
[Version] [2]
[Protocol] [3]
[Players] [4]/[5]
'''

save_server_with_bot = f'[Checker] [6]\n'

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

    def write(self, type, *data):
        if type == 'save_server':
            information = save_server

            for num, i in enumerate(data):
                information = information.replace(f'[{str(num)}]', str(i))

        if type == 'save_server_with_bot':
            for num, i in enumerate(data):
                information = save_server

                for num, i in enumerate(data):
                    information = information.replace(f'[{str(num)}]', str(i))
                
                information = f'{information}{save_server_with_bot.replace(f"[{str(num)}]", str(i))}'

        if type == 'save_timed_out_server':
            information = save_timed_out_server.replace('[0]', data[0])

        if type == 'save_player':
            information = save_player.replace('[0]', data[0])
            information = information.replace('&f&l', ''
                                    ).replace('&a', 'ONLINE: '
                                    ).replace('&c', 'OFFLINE: '
                                    ).replace('&5', 'CUSTOMIZED: ')
            
        if type == 'save_player_log':
            information = save_player_log.replace('[0]', data[0]).replace("[1]", data[1])
            information = information.replace('&f&l', ''
                                    ).replace('&a', 'ONLINE: '
                                    ).replace('&c', 'OFFLINE: '
                                    ).replace('&5', 'CUSTOMIZED: ')

        if type == 'save_data_from_fakesrv':
            information = data[0]

        if type == 'save_rcon_password':
            information = f'[!] RCON Password: {data[0]}'

        WriteFile(self.file, False, 'a', information)