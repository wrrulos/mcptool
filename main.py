#!/usr/bin/env python3

import os
import psutil
import subprocess
import time

from utils.banners.BannerMessages import *
from utils.banners.PrintBanner import print_banner
from utils.color.TextColor import paint
from utils.commands.Aternos import aternos_command
from utils.commands.AuthMe import authme_command
from utils.commands.Bungee import bungee_command
from utils.commands.Clear import clear_command
from utils.commands.Checker import checker_command
from utils.commands.Connect import connect_command
from utils.commands.DNSLookup import dnslookup_command
from utils.commands.Discord import discord_command
from utils.commands.FakeProxy import fakeproxy_command
from utils.commands.Help import help_command
from utils.commands.IPInfo import ipinfo_command
from utils.commands.Kick import kick_command
from utils.commands.KickAll import kickall_command
from utils.commands.Language import language_command
from utils.commands.Listening import listening_command
from utils.commands.Player import player_command
from utils.commands.PlayerLogs import playerlogs_command
from utils.commands.RConnect import rconnect_command
from utils.commands.Rcon import rcon_command
from utils.commands.ReverseIP import reverseip_command
from utils.commands.Scan import scan_command
from utils.commands.Search import search_command
from utils.commands.SendCommand import sendcommand_command
from utils.commands.Server import server_command
from utils.commands.Velocity import velocity_command
from utils.commands.WebSearch import websearch_command
from utils.checks.CommandArguments import check_command_arguments
from utils.gets.Language import language
from utils.managers.Dependencies import Dependencies
from utils.managers.Settings import SettingsManager
from utils.pid.KillPID import kill_pid
from utils.updates.Files import update_files
from utils.updates.MCPTool import update_mcptool
from utils.updates.Proxies import update_proxies

# Dictionary containing the list of MCPTool commands
commands = {
    'help': help_command,
    'cls': clear_command,
    'clear': clear_command,
    'server': server_command,
    'player': player_command,
    'ipinfo': ipinfo_command,
    'reverseip': reverseip_command,
    'dnslookup': dnslookup_command,
    'search': search_command,
    'websearch': websearch_command,
    'aternos': aternos_command,
    'scan': scan_command,
    'checker': checker_command,
    'listening': listening_command,
    'playerlogs': playerlogs_command,
    'bungee': bungee_command,
    'velocity': velocity_command,
    'fakeproxy': fakeproxy_command,
    'connect': connect_command,
    'rconnect': rconnect_command,
    'rcon': rcon_command,
    'authme':  authme_command,
    'kick': kick_command,
    'kickall': kickall_command,
    'sendcmd': sendcommand_command,
    'language': language_command,
    'discord': discord_command
}


def change_last_command(command):
    """
    change the last command of the 
    RichPresence status.

    Parameters:
    command (str): Command.
    """

    with open('utils/presence/RichPresence.command', 'w+') as f:
        f.truncate(0)
        f.write(command.capitalize())


def menu():
    """
    Allows the user to use the commands of the tool 
    through inputs.
    """

    if settings['RICH_PRESENCE']:
        subprocess.Popen(f'{settings["PYTHON_COMMAND"]} utils/presence/RichPresence.py {settings["CURRENT_VERSION"].split("///")[1]}', stdout=subprocess.PIPE, shell=True)

    while True:
        try:
            paint(f'\n    {language["script"]["INPUT"]}', end='')
            arguments = input().split()

            if len(arguments) > 0:
                try:
                    command = arguments[0].lower()

                    if command not in commands:
                        paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["INVALID_COMMAND"]}')

                    if command in commands and check_command_arguments(command, arguments):
                        change_last_command(command)
                        commands[command](*arguments[1:])

                except IndexError:
                    paint(f'\n    {language["script"]["PREFIX"]}{language["other_messages"]["INVALID_COMMAND"]}')

        except EOFError:
            pass

        except KeyboardInterrupt:
            try:
                if settings['RICH_PRESENCE']:
                    rich_presence_process = None
                    processes = [p for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']]

                    for p in processes:
                        if 'RichPresence.py' in str(p.cmdline()):
                            rich_presence_process = p
                            break

                    if rich_presence_process:
                        rich_presence_pid = rich_presence_process.pid
                        kill_pid(rich_presence_pid)

            except (KeyboardInterrupt, EOFError):
                pass

            break


if __name__ == '__main__':
    sm = SettingsManager()
    d = Dependencies()
    settings = sm.read('settings')
    mcptool_version = settings['CURRENT_VERSION'].split('///')[1]
    
    try:
        subprocess.run(f'cls || clear', shell=True)
        print_banner(f'pickaxe{settings["TYPE_OF_BANNERS"]}')
        time.sleep(0.5)
        dependencies = d.check_dependencies()

        if dependencies:
            if os.name == 'nt':
                subprocess.run(f'title {language["script"]["TITLE"]}', shell=True)

            update_mcptool()
            subprocess.run(f'cls || clear', shell=True)
            print_banner('updates')
            change_last_command('In the main menu')
            update_files()

            if settings['CHECK_PROXY_VERSIONS']:
                update_proxies()
                time.sleep(1)

            print_banner(f'presentation{settings["TYPE_OF_BANNERS"]}', presentation_mcptool, presentation_description, presentation_credits)
            time.sleep(2)

            subprocess.run('cls || clear', shell=True)
            print_banner('main', menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3, menu_message4, menu_message5, menu_message6, menu_message7)

    except KeyboardInterrupt:
        subprocess.run('cls || clear', shell=True)
        print_banner('main', menu_message1, menu_message2.replace('[0]', mcptool_version), menu_message3, menu_message4, menu_message5, menu_message6, menu_message7)

    menu()
