#!/usr/bin/env python3

import os
import subprocess
import time
import sys

from utils.banners.banner_messages import *
from utils.banners.print_banner import print_banner
from utils.color.text_color import paint
from utils.checks.check_termux import check_termux
from utils.termux.fix_dnspython import fix_dnspython
from utils.commands.login_command import login_command
from utils.commands.waterfall_command import waterfall_command
from utils.commands.clear_command import clear_command
from utils.commands.checker_command import checker_command
from utils.commands.connect_command import connect_command
from utils.commands.dnslookup_command import dnslookup_command
from utils.commands.discord_command import discord_command
from utils.commands.fakeproxy_command import fakeproxy_command
from utils.commands.help_command import help_command
from utils.commands.ipinfo_command import ipinfo_command
from utils.commands.kick_command import kick_command
from utils.commands.kickall_command import kickall_command
from utils.commands.language_command import language_command
from utils.commands.listening_command import listening_command
from utils.commands.player_command import player_command
from utils.commands.playerlogs_command import playerlogs_command
from utils.commands.pinlogin_command import pinlogin_command
from utils.commands.rcon_command import rcon_command
from utils.commands.rconbrute_command import rconbrute_command
from utils.commands.reverseip_command import reverseip_command
from utils.commands.scan_command import scan_command
from utils.commands.subdomains_command import subdomains_command
from utils.commands.search_command import search_command
from utils.commands.sendcommand_command import sendcommand_command
from utils.commands.server_command import server_command
from utils.commands.velocity_command import velocity_command
from utils.commands.websearch_command import websearch_command
from utils.checks.check_command_argument import check_command_arguments
from utils.managers.language_manager import language_manager
from utils.managers.dependencies_manager import Dependencies
from utils.managers.config_manager import config_manager
from utils.commands.reload_command import reload_command
from utils.pid.kill_pid import kill_pid
from utils.updates.mcptool_update import update_mcptool
from utils.updates.proxies_update import update_proxies
from utils.gets.get_spaces import get_spaces

# Dictionary containing the list of MCPTool commands
commands = {
    **dict.fromkeys(['cls', 'clear'], clear_command),
    **dict.fromkeys(['00', 'help'], help_command),
    **dict.fromkeys(['01', 'server'], server_command),
    **dict.fromkeys(['02', 'player'], player_command),
    **dict.fromkeys(['03', 'ipinfo'], ipinfo_command),
    **dict.fromkeys(['04', 'reverseip'], reverseip_command),
    **dict.fromkeys(['05', 'dnslookup'], dnslookup_command),
    **dict.fromkeys(['06', 'search'], search_command),
    **dict.fromkeys(['07', 'websearch'], websearch_command),
    **dict.fromkeys(['08', 'scan'], scan_command),
    **dict.fromkeys({'09', 'subdomains'}, subdomains_command),
    **dict.fromkeys(['10', 'checker'], checker_command),
    **dict.fromkeys(['11', 'listening'], listening_command),
    **dict.fromkeys(['12', 'playerlogs'], playerlogs_command),
    **dict.fromkeys(['13', 'waterfall'], waterfall_command),
    **dict.fromkeys(['14', 'velocity'], velocity_command),
    **dict.fromkeys(['15', 'fakeproxy'], fakeproxy_command),
    **dict.fromkeys(['16', 'connect'], connect_command),
    **dict.fromkeys(['17', 'rcon'], rcon_command),
    **dict.fromkeys(['18', 'rconbrute'], rconbrute_command),
    **dict.fromkeys(['19', 'login'], login_command),
    **dict.fromkeys(['20', 'pinlogin'], pinlogin_command),
    **dict.fromkeys(['21', 'kick'], kick_command),
    **dict.fromkeys(['22', 'kickall'], kickall_command),
    **dict.fromkeys(['23', 'sendcmd'], sendcommand_command),
    **dict.fromkeys(['24', 'discord'], discord_command),
    **dict.fromkeys(['25', 'language'], language_command),
    **dict.fromkeys(['26', 'reload'], reload_command)
}


def change_last_command(command):
    """
    change the last command of the 
    RichPresence status.

    Parameters:
        command (str): Command.
    """

    with open('utils/presence/richPresence.command', 'w+') as f:
        f.truncate(0)
        f.write(command.capitalize())


def menu():
    """
    Allows the user to use the commands of the tool 
    through inputs.
    """

    if os.name == 'nt':
        subprocess.run(f'title {language_manager.language["title"]}', shell=True)

    if not check_termux():
        if config_manager.config['richPresence']:
            subprocess.Popen(
                f'{sys.executable} utils/presence/rich_presence.py {config_manager.config["currentVersion"].split("///")[1]}',
                stdout=subprocess.PIPE, shell=True
            )

    while True:
        try:
            if not check_termux():
                paint(f'\n{get_spaces()}{language_manager.language["input"]}', end='')

            else:
                paint(f'\n {language_manager.language["termux_input"]}', end='')

            arguments = input().split()

            if len(arguments) > 0:
                try:
                    command = arguments[0].lower()

                    if command not in commands:
                        paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["invalidCommand"]}')

                    if command in commands and check_command_arguments(command, arguments):
                        if not check_termux():
                            change_last_command(command)

                        commands[command](*arguments[1:])

                except IndexError:
                    paint(f'\n{get_spaces()}{language_manager.language["prefix"]}{language_manager.language["invalidCommand"]}')

        except EOFError:
            pass

        except KeyboardInterrupt:
            try:
                if not check_termux():
                    import psutil

                    if config_manager.config['richPresence']:
                        rich_presence_process = None
                        processes = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]

                        for p in processes:
                            if 'rich_presence.py' in str(p.cmdline()):
                                rich_presence_process = p
                                break

                        if rich_presence_process:
                            rich_presence_pid = rich_presence_process.pid
                            kill_pid(str(rich_presence_pid))

            except (KeyboardInterrupt, EOFError):
                pass

            break


if __name__ == '__main__':
    d = Dependencies()
    mcptool_version = config_manager.config['currentVersion'].split('///')[1]
    banner_name = 'main' if not check_termux() else 'main_termux'
    pickaxe_banner_name = f'pickaxe{config_manager.config["typeOfBanners"]}' if not check_termux() else 'pickaxe_termux'
    presentation_banner_name = f'presentation{config_manager.config["typeOfBanners"]}' if not check_termux() else 'presentation_termux'
    
    try:
        if check_termux():
            fix_dnspython()

        subprocess.run(f'cls || clear', shell=True)
        print_banner(pickaxe_banner_name)
        time.sleep(0.5)
        dependencies = d.check_dependencies()

        if dependencies:
            update_mcptool()
            subprocess.run(f'cls || clear', shell=True)
            change_last_command('In the main menu')

            if config_manager.config['checkProxyVersions']:
                update_proxies()
                time.sleep(1)
                
            print_banner(
                presentation_banner_name, presentation_mcptool,
                presentation_description, presentation_credits
            )

            time.sleep(2)
            subprocess.run('clear || cls', shell=True)

            print_banner(
                banner_name, menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3,
                menu_message4, menu_message5, menu_message6, menu_message7
            )

    except KeyboardInterrupt:
        subprocess.run('clear || cls', shell=True)
        print_banner(
            banner_name, menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3,
            menu_message4, menu_message5, menu_message6, menu_message7
        )

    menu()
