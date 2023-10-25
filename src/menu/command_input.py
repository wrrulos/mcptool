import sys

from src.decoration.paint import paint
from src.decoration.print_banner import print_banner
from src.managers.json_manager import JsonManager
from src.menu.commands import commands
from src.utilities.get_utilities import GetUtilities
from src.utilities.check_utilities import CheckUtilities
from src.utilities.argument_checker import ArgumentChecker
from src.presence.rich_presence import RichPresenceUpdater


class CommandInput():
    @staticmethod
    def command_input(api_process):
        # Display the main menu banner with a welcome message.
        version = JsonManager.get('currentVersion')
        discord_presence = '✔️' if JsonManager.get('discordPresence') else '❌'
        bot = '✔️' if JsonManager.get(['minecraftServerOptions', 'checkServerLoginWithABot']) else '❌'
        proxy = '✔️' if JsonManager.get(['minecraftServerOptions', 'proxy']) else '❌'

        if CheckUtilities.check_termux():
            # Display the Termux-compatible menu banner.
            print_banner('menu_termux', GetUtilities.get_translated_text(['banners', 'menu_termux', 'message1']), GetUtilities.get_translated_text('credits'), version, GetUtilities.get_translated_text(['banners', 'menu_termux', 'message3']))
        
        else:
            # Display the regular menu banner.
            print_banner('menu', GetUtilities.get_translated_text(['banners', 'menu', 'message1']), GetUtilities.get_translated_text(['banners', 'menu', 'message2']), version, discord_presence, bot, proxy)
            
        while True:
            try:
                # Prompt the user for input.
                paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["input"])}', end='')
                arguments = input().split()

                if len(arguments) > 0:
                    command = arguments[0].lower()

                    if command not in commands:
                        # Display an error message for an invalid command.
                        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["invalidCommand"])}')

                    if command in commands and ArgumentChecker.check_arguments(command, arguments):
                        # Execute the command if it is recognized.
                        commands[command](*arguments[1:])

                        if not CheckUtilities.check_termux() and True:
                            # Update the last executed command for rich presence (if applicable).
                            RichPresenceUpdater.change_last_command(command)

            except (RuntimeError, EOFError):
                pass

            except KeyboardInterrupt:
                if api_process is not None:
                    api_process.terminate()
                    
                sys.exit()