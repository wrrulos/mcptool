import subprocess
import time

from utils.checks.check_encoding import check_encoding
from utils.color.text_color import paint
from utils.managers.language_manager import language_manager
from utils.managers.config_manager import config_manager
from utils.writefile.write_file import WriteFile
from utils.gets.get_spaces import get_spaces


def start_waterfall(server):
    """ 
    Start the waterfall.jar that is necessary 

    Args:
        server (str): Server IP and port
    """

    try:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["configuring"]}')
        time.sleep(1)

        with open('utils/otherfiles/waterfall_settings', 'r', encoding=check_encoding('utils/otherfiles/waterfall_settings')) as f:
            waterfall_settings = f.read()

        waterfall_settings = waterfall_settings.replace('[[PORT]]', config_manager.config['proxyConfig']['waterfallPort']).replace('[[ADDRESS]]', server)
        port = config_manager.config['proxyConfig']['waterfallPort']

        WriteFile(f'utils/waterfall/proxy/config.yml', True, 'w+', waterfall_settings)
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["starting"]}')
        time.sleep(0.5)
        paint(f'\n{get_spaces()}{language_manager.language["proxyMessages"]["proxyServerStarted"].replace("[0]", f"""127.0.0.1:{port}""")}')
        subprocess.run(f'cd utils/waterfall/proxy/ && {config_manager.config["commands"]["waterfall"]}', stdout=subprocess.PIPE, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["proxyMessages"]["stopping"]}')
        return
