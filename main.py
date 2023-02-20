#!/usr/bin/python3

import subprocess
import time
import os

from utils.checks.CommandArguments import check_command_arguments
from utils.waterfall.StartWaterfall import start_waterfall
from utils.commands.Help import help_command
from utils.commands.Server import server_command
from utils.commands.Player import player_command
from utils.commands.IPInfo import ipinfo_command
from utils.commands.DNSLookup import dnslookup_command
from utils.commands.Search import search_command
from utils.commands.Scan import scan_command
from utils.commands.Host import host_command
from utils.commands.Checker import checker_command
from utils.commands.Listening import listening_command
from utils.commands.Connect import connect_command
from utils.commands.RConnect import rconnect_command
from utils.commands.Rcon import rcon_command
from utils.commands.AuthMe import authme_command
from utils.commands.Kick import kick_command
from utils.commands.KickAll import kickall_command
from utils.commands.SendCommand import sendcommand_command
from utils.commands.Language import language_command
from utils.commands.Discord import discord_command
from utils.managers.Dependencies import Dependencies
from utils.managers.Settings import SettingsManager
from utils.banners.PrintBanner import print_banner
from utils.updates.MCPTool import update_mcptool
from utils.gets.Language import language
from utils.color.TextColor import paint

check_for_waterfall_updates = -1

sm = SettingsManager()
d = Dependencies()


def menu():
    """
    This function contains an input that allows the user to
    execute the different MCPTool commands.
    """

    global check_for_waterfall_updates, rich_presence

    while True:
        try:
            paint(f'\n    {language["script"]["INPUT"]}', end='')
            arguments = input().split()

            try:
                command = arguments[0].lower()

            except IndexError:
                paint(f'\n    {language["script"]["PREFIX"]}{language["script"]["INVALID_COMMAND"]}')
                continue

            if command == 'help':
                help_command()

            elif command == 'clear':
                subprocess.run('cls || clear', shell=True)
                print_banner('main', message1, message2, message3, message4)

            elif command == 'server':
                if check_command_arguments(command, arguments):
                    server_command(arguments[1])

            elif command == 'player':
                if check_command_arguments(command, arguments):
                    player_command(arguments[1])

            elif command == 'ipinfo':
                if check_command_arguments(command, arguments):
                    ipinfo_command(arguments[1])

            elif command == 'dnslookup':
                if check_command_arguments(command, arguments):
                    dnslookup_command(arguments[1])

            elif command == 'search':
                if check_command_arguments(command, arguments):
                    search_command(arguments)

            elif command == 'scan':
                if check_command_arguments(command, arguments):
                    try:
                        scan_command(arguments[1], arguments[2], arguments[3], arguments[4].lower(), arguments[5])

                    except IndexError:
                        scan_command(arguments[1], arguments[2], arguments[3], arguments[4].lower())

            elif command == 'host':
                if check_command_arguments(command, arguments):
                    try:
                        host_command(arguments[1], arguments[2], arguments[3], arguments[4].lower(), arguments[5])

                    except IndexError:
                        host_command(arguments[1], arguments[2], arguments[3], arguments[4].lower())

            elif command == 'checker':
                if check_command_arguments(command, arguments):
                    try:
                        checker_command(arguments[1], arguments[2], arguments[3])

                    except IndexError:
                        checker_command(arguments[1], arguments[2])

            elif command == 'listening':
                if check_command_arguments(command, arguments):
                    listening_command(arguments[1])

            elif command == 'bungee':
                if check_command_arguments(command, arguments):
                    check_for_waterfall_updates += 1

                    if check_for_waterfall_updates < 1:
                        start_waterfall(arguments[1], True)

                    else:
                        start_waterfall(arguments[1], False)

            elif command == 'poisoning':
                if check_command_arguments(command, arguments):
                    check_for_waterfall_updates += 1

                    if check_for_waterfall_updates < 1:
                        start_waterfall(arguments[1], True, True)

                    else:
                        start_waterfall(arguments[1], False, True)

            elif command == 'connect':
                if check_command_arguments(command, arguments):
                    try:
                        connect_command(arguments[1], arguments[2], arguments[3], arguments[4])

                    except IndexError:
                        connect_command(arguments[1], arguments[2], arguments[3])

            elif command == 'rconnect':
                if check_command_arguments(command, arguments):
                    rconnect_command(arguments[1], arguments[2])

            elif command == 'rcon':
                if check_command_arguments(command, arguments):
                    try:
                        rcon_command(arguments[1], arguments[2], arguments[3])

                    except IndexError:
                        rcon_command(arguments[1], arguments[2])

            elif command == 'authme':
                if check_command_arguments(command, arguments):
                    try:
                        authme_command(arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])

                    except IndexError:
                        authme_command(arguments[1], arguments[2], arguments[3], arguments[4])

            elif command == 'kick':
                if check_command_arguments(command, arguments):
                    try:
                        kick_command(arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])

                    except IndexError:
                        kick_command(arguments[1], arguments[2], arguments[3], arguments[4])

            elif command == 'kickall':
                if check_command_arguments(command, arguments):
                    try:
                        kickall_command(arguments[1], arguments[2], arguments[3], arguments[4])

                    except IndexError:
                        kickall_command(arguments[1], arguments[2], arguments[3])

            elif command == 'sendcmd':
                if check_command_arguments(command, arguments):
                    try:
                        sendcommand_command(arguments[1], arguments[2], arguments[3], arguments[4], arguments[5])

                    except IndexError:
                        sendcommand_command(arguments[1], arguments[2], arguments[3], arguments[4])

            elif command == 'language':
                if check_command_arguments(command, arguments):
                    language_command(arguments[1])

            elif command == 'discord':
                discord_command()

            else:
                paint(f'\n    {language["script"]["PREFIX"]}{language["script"]["INVALID_COMMAND"]}')

        except EOFError:
            pass

        except KeyboardInterrupt:
            if settings['RICH_PRESENCE']:
                rich_presence.kill()

            break


if __name__ == '__main__':
    subprocess.run(f'cls || clear', shell=True)
    settings = sm.read('settings')
    print_banner(f'pickaxe{settings["TYPE_OF_BANNERS"]}')
    dependencies = d.check_dependencies()

    if dependencies:
        if os.name == 'nt':
            subprocess.run(f'title {language["script"]["TITLE"]}', shell=True)

        mcptool = language['banners']['presentation']['MCPTOOL']
        description = language['banners']['presentation']['DESCRIPTION']
        credits = language['banners']['presentation']['CREDITS']

        message1 = language['banners']['menu']['MESSAGE1']
        message2 = language['banners']['menu']['MESSAGE2']
        message3 = language['banners']['menu']['MESSAGE3']
        message4 = language['banners']['menu']['MESSAGE4']
        message5 = language['banners']['first-time-main']['MESSAGE1']
        message6 = language['banners']['first-time-main']['MESSAGE2']
        message7 = language['banners']['first-time-main']['MESSAGE3']

        update_mcptool()
        print_banner(f'presentation{settings["TYPE_OF_BANNERS"]}', mcptool, description, credits)
        time.sleep(3)

        if settings['RICH_PRESENCE']:
            rich_presence = subprocess.Popen(f'{settings["PYTHON_COMMAND"]} utils/presence/RichPresence.py', stdout=subprocess.PIPE, shell=True)

        subprocess.run(f'cls || clear', shell=True)
        print_banner('first-time-main', message1, message2, message3, message4, message5, message6, message7)
        menu()
