import multiprocessing
import subprocess
import threading
import time
import sys

from src.decoration.print_banner import print_banner
from src.updater.mcptool_updater import MCPToolUpdater
from src.updater.proxy_updater import ProxyUpdater
from src.menu.command_input import CommandInput
from src.managers.json_manager import JsonManager
from src.utilities.check_utilities import CheckUtilities
from src.utilities.get_utilities import GetUtilities
from src.termux.fix_dnspython import fix_dnspython
from src.presence.rich_presence import RichPresenceUpdater
from src.api.api import run_flask_app


class Startup():
    @staticmethod
    def run():
        """
        Initialize and start various components of the application.
        
        This method performs the following tasks:
        - Checks for updates and displays update banners.
        - Updates proxy software if configured to do so.
        - Starts a separate process for Discord Rich Presence (if not on Termux).
        - Initializes and starts a local API if configured to use 'localhost'.
        - Starts the command input loop.
        """

        # Fix dnspython error in termux.
        if CheckUtilities.check_termux():
            fix_dnspython()

        # In case the entered API is invalid, it sets mcsrvstat.us to default.
        if JsonManager.get('api') not in ['localhost', 'mcsrvstat.us', 'mcstatus.io']:
            settings = JsonManager.load_json('./config/config.json')
            settings['api'] = 'mcsrvstat.us'
            JsonManager.save_json(settings, './config/config.json')

        # Check if a new version of MCPTool is available and display an update banner if necessary.
        MCPToolUpdater.show_banner_update()

        # Check for proxy server updates.
        if JsonManager.get(['proxyConfig', 'updateProxy']):
            ProxyUpdater.update_proxies()

        # Start the discord presence.
        if not CheckUtilities.check_termux() and JsonManager.get('discordPresence'):
            rich_presence_thread = threading.Thread(target=RichPresenceUpdater.update_rich_presence, args=('1127920414383943801', '4.1.0'))
            rich_presence_thread.daemon = True
            rich_presence_thread.start()

        # Initialize a variable to store the API process.
        api_process = None

        if JsonManager.get('api') == 'localhost':
            # Start the local API to query data from Minecraft servers.
            try:
                starting_api_banner_name = f'starting_api' if not CheckUtilities.check_termux() else 'starting_api_termux'
                print_banner(starting_api_banner_name)
                time.sleep(1)

                # Check if the API is already running on the specified port.
                if not CheckUtilities.check_local_port(JsonManager.get('local_api_port')):
                    # If not running, create a new process for the API.
                    api_process = multiprocessing.Process(target=run_flask_app)
                    api_process.daemon = True
                    api_process.start()

            except KeyboardInterrupt:
                settings = JsonManager.load_json('./config/config.json')
                settings['api'] = 'mcsrvstat.us'
                JsonManager.save_json(settings, './config/config.json')
                api_process = None

        try:
            presentation_banner_name = f'presentation' if not CheckUtilities.check_termux() else 'presentation_termux'
            print_banner(presentation_banner_name, GetUtilities.get_translated_text(['banners', 'presentation', 'message1']), GetUtilities.get_translated_text(['banners', 'presentation', 'message1']), GetUtilities.get_translated_text('credits'))
            time.sleep(2)

        except KeyboardInterrupt:
            pass

        CommandInput.command_input(api_process)

