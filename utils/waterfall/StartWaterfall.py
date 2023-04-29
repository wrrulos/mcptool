import subprocess
import time

from utils.checks.Encoding import check_encoding
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager
from utils.writefile.WriteFile import WriteFile


def start_waterfall(server):
    """ 
    Start the waterfall.jar that is necessary 

    Parameters:
        server (str): Server IP and port
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    try:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["CONFIGURING"]}')
        time.sleep(1)

        with open('utils/otherfiles/waterfall_settings', 'r', encoding=check_encoding('utils/otherfiles/waterfall_settings')) as f:
            waterfall_settings = f.read()

        waterfall_settings = waterfall_settings.replace('[[PORT]]', settings['BUNGEE_PORT']
                                          ).replace('[[ADDRESS]]', server)
        port = settings['BUNGEE_PORT']

        WriteFile(f'utils/waterfall/proxy/config.yml', True, 'w+', waterfall_settings)
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["STARTING"]}')
        time.sleep(0.5)
        proxy = subprocess.Popen(f'cd utils/waterfall/proxy/ && {settings["WATERFALL_COMMAND"]}', stdout=subprocess.PIPE, shell=True)
        paint(f'\n    {language["proxy_messages"]["PROXY_SERVER_STARTED"].replace("[0]", f"""127.0.0.1:{port}""")}')

    except KeyboardInterrupt:
        paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["STOPPING"]}')
        return

    while True:
        try:
            time.sleep(1)

        except KeyboardInterrupt:
            paint(f'\n    {language["script"]["PREFIX"]}{language["proxy_messages"]["STOPPING"]}')
            proxy.kill()
            return
