from utils.sounds.play_sound import play_sound
from utils.color.text_color import paint
from utils.managers.config_manager import config_manager
from utils.managers.language_manager import language_manager
from utils.minecraft.check_server import check_server
from utils.gets.get_spaces import get_spaces


def check_servers(servers, bot, proxy_file, logs):
    """
    Check a list of Minecraft servers and display the results.

    Parameters:
        servers (list): A list of Minecraft servers to check.
        bot: The bot instance.
        proxy_file (str): The path to the proxy file.
        logs (str): The path to the logs file.
    """
    
    servers_found = 0
    timed_out_servers_found = 0

    for server in servers:
        check = check_server(server, bot, proxy_file, logs)

        if check == 'CtrlC':
            paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
            return

        if check is None:
            return

        if check:
            servers_found += 1

        else:
            timed_out_servers_found += 1

    if config_manager.config['scannerOptions']['showTimedOutServers'] and timed_out_servers_found >= 1:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["scanFinished2"].replace("[0]", str(servers_found)).replace("[1]", str(timed_out_servers_found))}')

    else:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["scanFinished1"].replace("[0]", str(servers_found))}')

    if config_manager.config['sounds']:
        play_sound('sound1')
