import time
import re

from utils.minecraft.bot_messages import replace_messages
from utils.minecraft.server_data import GetDataFromMinecraftServer
from utils.minecraft.send_bot import send_bot
from utils.minecraft.show_server import show_server, show_timed_out_server
from utils.managers.config_manager import config_manager
from utils.mccolor import mcremove


def check_server(ip, bot=False, proxy_file=None, logs=None, timeout=config_manager.config['scannerOptions']['showTimedOutServers']):
    """
    Save and show server state

    Args:
        ip (str): IP address (the port is also possible) of the server
        bot (bool): Boolean value that decides whether to send a bot or not
        proxy_file (str): Proxy File (socks5) that the bot will use to connect
        logs (str): Object Logs created above to use the .write function

    Returns:
        bool: Boolean value that checks if the server is on
    """

    try:
        server_data = GetDataFromMinecraftServer(server=ip)
        data = server_data.get_information()

        if data == 'CtrlC':
            return 'CtrlC'

        output = None

        if data is not None:
            if bot:
                output = send_bot(data[1], data[4], proxy_file)

                if output is None or output == 'CtrlC':
                    if output is None:
                        time.sleep(1)

                    return output
                
                output = replace_messages(output)
                output = mcremove(output)
                pattern = re.compile(r'\x1b\[[0-9;]*m')
                clean_output = pattern.sub('', output)
                logs.write('save_server', data, clean_output)

            else:
                logs.write('save_server', data)

            show_server(data, output)
            return True

        else:
            if config_manager.config['scannerOptions']['showTimedOutServers']:
                ip = f'{ip[0]}:{ip[1]}' if len(ip) == 2 else ip
                show_timed_out_server(ip)

            logs.write('save_timed_out_server', ip)
            return False

    except KeyboardInterrupt:
        return 'CtrlC'
