import time

from utils.minecraftserver.ShowServer import show_server, show_timed_out_server
from utils.color.ColoredCharacters import replace_colors, remove_colors
from utils.color.ColoredOutput import get_colored_output
from utils.minecraftserver.ServerData import mcstatus
from utils.managers.Settings import SettingsManager
from utils.minecraftserver.SendBot import send_bot

sm = SettingsManager()
settings = sm.read('settings')


def check_server(ip, bot, proxy, logs):
    """
    Save and show server state

    :param ip: IP address of the server
    :param bot: Boolean value that decides whether to send a bot or not
    :param proxy: Socks5 proxy that the bot will use to connect
    :param logs: Object Logs created above to use the .write function
    :return: Boolean value that checks if the server is on
    """

    data = mcstatus(ip)
    output = None

    try:
        if data is not None:
            if bot:
                if data[2] == -1:
                    return False
                
                output = send_bot(ip, data[2], proxy)

                if output is None or output == 'CtrlC':
                    if output is None:
                        time.sleep(1)

                    return output
                
                output = get_colored_output(output)              
                logs.write('save_server_with_bot', ip, data[6], data[7], data[2], data[3], data[4], remove_colors(output))

            else:
                logs.write('save_server', ip, data[6], data[7], data[2], data[3], data[4])

            show_server(ip, data[0], data[1], data[2], data[3], data[4], data[5], replace_colors(output))
            return True

        else:
            if settings['SHOW_TIMED_OUT_SERVERS']:
                show_timed_out_server(ip)
            
            logs.write('save_timed_out_server', ip)
            return False

    except KeyboardInterrupt:
        return 'CtrlC'