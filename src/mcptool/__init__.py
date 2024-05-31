#!/usr/bin/env python3

import subprocess
import threading
import random
import struct
import shutil
import time
import os
import pypresence

from loguru import logger
from mccolors import mcwrite, mcreplace

# Import the MCPToolPath class
from .modules.utilities.path.mcptool_path import MCPToolPath

# Remove the default logger
logger.remove()

# Set the logging configuration
logger.add(os.path.join(MCPToolPath().get(), 'debug.log'),
    level='INFO',
    format='[{time} {level} - {file}, {line}] ⮞ <level>{message}</level>',
    rotation="30 MB"
)

# Check if the files exist
MCPToolPath().check_files()

# Utilities
from .modules.utilities.managers.language_manager import LanguageManager as LM
from .modules.utilities.banners.banners import MCPToolBanners, InputBanners
from .modules.utilities.banners.show_banner import ShowBanner
from .modules.commands.clear import Command as ClearCommand
from .modules.commands.help import Command as HelpCommand
from .modules.commands.discord import Command as DiscordCommand
from .modules.commands.server import Command as ServerCommand
from .modules.commands.uuid import Command as UUIDCommand
from .modules.commands.ipinfo import Command as IPInfoCommand
from .modules.commands.dnslookup import Command as DNSLookupCommand
from .modules.commands.resolver import Command as ResolverCommand
from .modules.commands.seeker import Command as SeekerCommand
from .modules.commands.scan import Command as ScanCommand
from .modules.commands.kick import Command as KickCommand
from .modules.commands.kickall import Command as KickAllCommand
from .modules.commands.listening import Command as ListeningCommand
from .modules.commands.bruteauth import Command as BruteAuthCommand
from .modules.commands.brutercon import Command as BruteRconCommand
from .modules.commands.connect import Command as ConnectCommand
from .modules.commands.proxy import Command as ProxyCommand
from .modules.commands.fakeproxy import Command as FakeProxyCommand
from .modules.commands.rcon import Command as RconCommand
from .modules.commands.checker import Command as CheckerCommand
from .modules.commands.sendcmd import Command as SendCmdCommand
from .modules.commands.subdomains import Command as SubdomainsCommand
from .modules.commands.language import Command as LanguageCommand
from .modules.utilities.constants import VERSION, MCPTOOL_DISCORD_CLIENT_ID, DISCORD_LINK, MCPTOOL_WEBSITE


class MCPTool:
    __version__: str = VERSION

    def __init__(self, commands_folder_path: str = 'src/mcptool/modules/commands'):
        self.commands_folder_path: str = commands_folder_path
        self.commands: dict = {}
        self.actual_command: str = f'Using MCPTool v{VERSION}'

    @logger.catch
    def run(self):
        # Notify the user that the tool is starting
        logger.info(f'MCPTool v{self.__version__} is starting...')

        # Load the commands
        self.commands = self._get_commands()

        # Update the rich presence in another thread
        rich_presence_thread = threading.Thread(target=self._update_rich_presence, args=([]))
        rich_presence_thread.daemon = True
        rich_presence_thread.start()

        # Start the command input
        self._command_input()

    @logger.catch
    def _command_input(self) -> None:
        """
        Method to manage the command line input
        """

        # Set the title on cmd
        if os.name == 'nt':
            subprocess.run('title MCPTool', shell=True, check=True)
            self._remove_python_files()

        # Select and show a random banner
        banner: str = MCPToolBanners.BANNERS[random.randint(0, len(MCPToolBanners.BANNERS) - 1)]
        ShowBanner(banner, clear_screen=True).show()

        while True:
            try:
                # Get the user input
                arguments: list = input(mcreplace(InputBanners.INPUT_1)).split()

                # Check if the arguments are empty
                if len(arguments) == 0:
                    continue

                # Get the command
                command_name: str = arguments[0].lower()

                # Check if the command is exit
                if command_name == "exit":
                    break

                # Check if the command exists
                if command_name not in self.commands:
                    mcwrite(LM().get(['commands', 'invalidCommand']))
                    continue

                try:
                    # Execute the command
                    command_instance = self.commands[command_name]
                    command_instance.execute(arguments[1:])
                    self.actual_command = f'Using the {command_name} command'

                except KeyboardInterrupt:
                    mcwrite(LM().get(['commands', 'ctrlC']))
                    continue

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                break

    @logger.catch
    def _get_commands(self) -> dict:
        """
        Method to get the commands

        Returns:
            dict: The commands
        """

        return {
            'clear': ClearCommand(),
            'help': HelpCommand(),
            'discord': DiscordCommand(),
            'server': ServerCommand(),
            'uuid': UUIDCommand(),
            'ipinfo': IPInfoCommand(),
            'dnslookup': DNSLookupCommand(),
            'resolver': ResolverCommand(),
            'seeker': SeekerCommand(),
            'scan': ScanCommand(),
            'kick': KickCommand(),
            'kickall': KickAllCommand(),
            'listening': ListeningCommand(),
            'bruteauth': BruteAuthCommand(),
            'brutercon': BruteRconCommand(),
            'connect': ConnectCommand(),
            'proxy': ProxyCommand(),
            'fakeproxy': FakeProxyCommand(),
            'rcon': RconCommand(),
            'checker': CheckerCommand(),
            'sendcmd': SendCmdCommand(),
            'subdomains': SubdomainsCommand(),
            'language': LanguageCommand()
        }

    @logger.catch
    def _update_rich_presence(self) -> None:
        """
        Method to update the rich presence
        """

        # Initialize the rich presence
        rpc: pypresence.Presence = pypresence.Presence(MCPTOOL_DISCORD_CLIENT_ID)

        # Set the start time
        start_time: int = int(time.time())

        try:
            # Connect to the Discord client
            rpc.connect()
            logger.info('Connected to the Discord client')

            while True:
               rpc.update(
                    state=self.actual_command,
                    details='Pentesting Tool for Minecraft',
                    start=start_time,
                    large_image='logo',
                    large_text='Pentesting Tool for Minecraft',
                    small_image='small_logo',
                    small_text=f'Version: {VERSION}',
                    buttons=[
                        {'label': 'Website', 'url': MCPTOOL_WEBSITE},
                        {'label': 'Discord', 'url': DISCORD_LINK}
                    ]
                )

               time.sleep(1)

        except (pypresence.exceptions.DiscordNotFound, struct.error, pypresence.exceptions.ServerError, pypresence.exceptions.ResponseTimeout) as e:
            logger.error(f'Failed to connect to the Discord client. Error: {e}. Retrying in 30 seconds...')
            time.sleep(30)
            self._update_rich_presence()

        except (KeyboardInterrupt, ValueError, RuntimeError, OSError):
            logger.error('Failed to connect to the Discord client. Retrying in 30 seconds...')
            pass

    @logger.catch
    def _remove_python_files(self) -> None:
        """
        Remove the python files in the AppData directory after the update
        """

        # Remove python files and lib folder in the AppData directory
        appdata_path: str = os.getenv('APPDATA')  #* %appdata%
        lib_folder_path: str = os.path.abspath(os.path.join(appdata_path, 'lib'))  #* %appdata%/lib

        if os.path.exists(lib_folder_path):
            shutil.rmtree(lib_folder_path)

        for file in os.listdir(appdata_path):
            if file == 'MCPToolUpdater.exe' or file == 'MCPTool-win64.msi':
                os.remove(os.path.join(appdata_path, file))

            if file.endswith('.dll'):
                if 'python' in file:
                    os.remove(os.path.join(os.getenv('APPDATA'), file))
