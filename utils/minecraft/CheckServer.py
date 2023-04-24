import time

from utils.minecraft.BotMessages import replace_messages
from utils.minecraft.ServerData import mcstatus
from utils.minecraft.SendBot import send_bot
from utils.minecraft.ShowServer import show_server, show_timed_out_server
from utils.managers.Settings import SettingsManager
from utils.mccolor import mcremove

sm = SettingsManager()
settings = sm.read('settings')


def check_server(ip, bot, proxy, logs, timeout=settings['SHOW_TIMED_OUT_SERVERS']):
    """
    Save and show server state

    Parameters:
    ip (str): IP address of the server
    bot (str): Boolean value that decides whether to send a bot or not
    proxy (str): Socks5 proxy that the bot will use to connect
    logs (str): Object Logs created above to use the .write function
    
    Returns:
    bool: Boolean value that checks if the server is on
    """

    data = mcstatus(ip)
    output = None

    try:
        if data is not None:
            if bot:                
                output = send_bot(ip, data[2], proxy)

                if output is None or output == 'CtrlC':
                    if output is None:
                        time.sleep(1)

                    return output
                
                output = replace_messages(output)              
                logs.write('save_server_with_bot', ip, data[6], data[7], data[2], data[3], data[4], mcremove(output))

            else:
                logs.write('save_server', ip, data[6], data[7], data[2], data[3], data[4])

            show_server(ip, data[0], data[1], data[2], data[3], data[4], data[5], output)
            return True

        else:
            if settings['SHOW_TIMED_OUT_SERVERS']:
                show_timed_out_server(ip)

            logs.write('save_timed_out_server', ip)
            return False

    except KeyboardInterrupt:
        return 'CtrlC'